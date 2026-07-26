#!/usr/bin/env python
"""Inventorying and ratcheting the temporary active Numba surface.

The migration baseline is intentionally monotonic: removing recorded Numba
coupling is allowed, while adding a new import, JIT site, CUDA module, or direct
``molsysmt.lib`` consumer fails the gate. The broader documentation, test,
configuration, and dependency surfaces are recorded for the eventual zero-Numba
cut but do not act as line-sensitive ratchets.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
BASELINE = REPO / "devtools" / "data" / "numba_surface_baseline.json"
SCHEMA = "molsysmt.numba-surface@1"
GUARDED_CATEGORIES = (
    "numba_imports",
    "jit_sites",
    "cuda_modules",
    "direct_lib_consumers",
)
NUMBA_TOKENS = ("numba", "llvmlite", "lazy_njit", "numba_")
CONTROL_TOKENS = (
    "configure.kernel",
    "kernel=",
    "warmup_numba",
    "compile_registered",
    "NUMBA_CACHE_DIR",
    "NumbaJit",
)


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _imported_module(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if isinstance(node, ast.ImportFrom):
        return [node.module or ""]
    return []


def _decorator_name(node: ast.AST) -> str:
    target = node.func if isinstance(node, ast.Call) else node
    parts = []
    while isinstance(target, ast.Attribute):
        parts.append(target.attr)
        target = target.value
    if isinstance(target, ast.Name):
        parts.append(target.id)
    return ".".join(reversed(parts))


def _qualified_functions(tree: ast.AST):
    def visit(nodes, parents=()):
        for node in nodes:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qualified = ".".join((*parents, node.name))
                yield node, qualified
                yield from visit(node.body, (*parents, node.name))
            elif isinstance(node, ast.ClassDef):
                yield from visit(node.body, (*parents, node.name))

    yield from visit(getattr(tree, "body", []))


def _is_jit_decorator(name: str) -> bool:
    leaf = name.rsplit(".", 1)[-1]
    return leaf in {
        "lazy_njit",
        "njit",
        "jit",
        "vectorize",
        "guvectorize",
    } or name.endswith("cuda.jit")


def _read_notebook_sources(path: Path) -> str:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return ""
    return "\n".join(
        "".join(cell.get("source", []))
        if isinstance(cell.get("source", []), list)
        else str(cell.get("source", ""))
        for cell in payload.get("cells", [])
    )


def _files_containing(
    root: Path,
    relative_root: str,
    suffixes: set[str],
    tokens: tuple[str, ...],
    *,
    excluded_parts: set[str] | None = None,
) -> list[str]:
    directory = root / relative_root
    if not directory.exists():
        return []
    excluded_parts = excluded_parts or set()
    output = []
    for path in sorted(directory.rglob("*")):
        if (
            not path.is_file()
            or path.suffix not in suffixes
            or excluded_parts.intersection(path.relative_to(root).parts)
        ):
            continue
        if path.suffix == ".ipynb":
            text = _read_notebook_sources(path)
        else:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
        normalized_text = text.lower()
        if any(token.lower() in normalized_text for token in tokens):
            output.append(_relative(path, root))
    return output


def collect_inventory(root: Path = REPO) -> dict:
    """Returning the deterministic active Numba migration inventory."""

    package = root / "molsysmt"
    numba_imports = []
    jit_sites = []
    cuda_modules = set()
    direct_lib_consumer_candidates = []
    coupled_lib_modules = set()
    runtime_control_files = set()

    for path in sorted(package.rglob("*.py")):
        relative = _relative(path, root)
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=relative)
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue

        imported_numba = False
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            for module in _imported_module(node):
                if module == "numba" or module.startswith("numba."):
                    imported_numba = True
                    numba_imports.append(f"{relative}::{module}")
                elif module == "llvmlite" or module.startswith("llvmlite."):
                    numba_imports.append(f"{relative}::{module}")
                if (
                    module == "molsysmt.lib"
                    or module.startswith("molsysmt.lib.")
                ) and not relative.startswith("molsysmt/lib/"):
                    direct_lib_consumer_candidates.append((relative, module))

        file_has_jit = False
        for function, qualified_name in _qualified_functions(tree):
            for decorator in function.decorator_list:
                name = _decorator_name(decorator)
                if _is_jit_decorator(name):
                    file_has_jit = True
                    jit_sites.append(f"{relative}::{qualified_name}::{name}")
                    if name.endswith("cuda.jit"):
                        cuda_modules.add(relative)

        if path.stem.endswith("_cuda") or (
            imported_numba and "cuda" in text
        ):
            cuda_modules.add(relative)
        if relative.startswith("molsysmt/lib/") and (
            imported_numba or file_has_jit
        ):
            module = relative.removesuffix(".py").replace("/", ".")
            coupled_lib_modules.add(module)
        if any(token in text for token in CONTROL_TOKENS):
            runtime_control_files.add(relative)

    direct_lib_consumers = {
        f"{relative}::{module}"
        for relative, module in direct_lib_consumer_candidates
        if any(
            module == coupled
            or coupled.startswith(f"{module}.")
            for coupled in coupled_lib_modules
        )
    }

    dependency_files = set()
    dependency_candidates = [root / "pyproject.toml"]
    dependency_candidates.extend(
        (root / "devtools" / "conda-envs").glob("*.yaml")
        if (root / "devtools" / "conda-envs").exists()
        else []
    )
    dependency_candidates.extend(
        (root / "devtools" / "conda-build").rglob("*")
        if (root / "devtools" / "conda-build").exists()
        else []
    )
    for path in dependency_candidates:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "numba" in text.lower() or "llvmlite" in text.lower():
            dependency_files.add(_relative(path, root))

    surfaces = {
        "runtime_reference_files": _files_containing(
            root,
            "molsysmt",
            {".py"},
            (*NUMBA_TOKENS, *CONTROL_TOKENS),
        ),
        "runtime_control_files": sorted(runtime_control_files),
        "dependency_files": sorted(dependency_files),
        "test_files": _files_containing(
            root,
            "tests",
            {".py"},
            NUMBA_TOKENS,
        ),
        "tool_files": _files_containing(
            root,
            "devtools",
            {".py", ".json", ".toml", ".yaml", ".yml"},
            (*NUMBA_TOKENS, *CONTROL_TOKENS),
        ),
        "build_files": _files_containing(
            root,
            ".github",
            {".yaml", ".yml"},
            (*NUMBA_TOKENS, *CONTROL_TOKENS),
        ),
        "experiment_files": _files_containing(
            root,
            "experiments",
            {".md", ".py", ".rs", ".toml", ".yaml", ".yml"},
            (*NUMBA_TOKENS, *CONTROL_TOKENS),
        ),
        "active_documentation_files": _files_containing(
            root,
            "docs",
            {".md", ".ipynb"},
            NUMBA_TOKENS,
            excluded_parts={"showcase"},
        ),
        "active_devguide_files": _files_containing(
            root,
            "devguide",
            {".md", ".ipynb"},
            NUMBA_TOKENS,
            excluded_parts={"archive"},
        ),
    }

    guarded = {
        "numba_imports": sorted(set(numba_imports)),
        "jit_sites": sorted(set(jit_sites)),
        "cuda_modules": sorted(cuda_modules),
        "direct_lib_consumers": sorted(direct_lib_consumers),
    }
    counts = {
        **{name: len(values) for name, values in guarded.items()},
        **{name: len(values) for name, values in surfaces.items()},
    }
    return {
        "schema": SCHEMA,
        "guarded": guarded,
        "surfaces": surfaces,
        "counts": counts,
    }


def compare_guarded(current: dict, baseline: dict) -> tuple[dict, dict]:
    """Returning newly added and resolved identities by guarded category."""

    added = {}
    resolved = {}
    for category in GUARDED_CATEGORIES:
        current_values = set(current["guarded"].get(category, []))
        baseline_values = set(baseline["guarded"].get(category, []))
        if current_values - baseline_values:
            added[category] = sorted(current_values - baseline_values)
        if baseline_values - current_values:
            resolved[category] = sorted(baseline_values - current_values)
    return added, resolved


def _write_baseline(inventory: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-baseline",
        action="store_true",
        help="replace the migration baseline with the current generated inventory",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the current generated inventory as JSON",
    )
    args = parser.parse_args()

    current = collect_inventory()
    if args.json:
        print(json.dumps(current, indent=2, sort_keys=True))
        return 0
    if args.write_baseline:
        _write_baseline(current, BASELINE)
        print(f"Wrote Numba surface baseline: {BASELINE.relative_to(REPO)}")
        return 0
    if not BASELINE.exists():
        print(
            "Numba surface audit FAILED: missing baseline; run with "
            "--write-baseline after review."
        )
        return 1

    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    if baseline.get("schema") != SCHEMA:
        print(
            "Numba surface audit FAILED: baseline schema "
            f"{baseline.get('schema')!r} != {SCHEMA!r}"
        )
        return 1

    added, resolved = compare_guarded(current, baseline)
    print("Active Numba migration surface:")
    for name, count in current["counts"].items():
        print(f"  {name}: {count}")
    print(
        "  resolved guarded identities since baseline: "
        f"{sum(len(values) for values in resolved.values())}"
    )
    if added:
        print("\nNumba surface audit FAILED: new guarded coupling:")
        for category, values in added.items():
            print(f"  {category}:")
            for value in values:
                print(f"    - {value}")
        return 1
    print("Numba surface ratchet: PASS (no new kernels or direct coupling)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
