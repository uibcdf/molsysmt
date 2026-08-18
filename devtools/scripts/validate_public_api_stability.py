#!/usr/bin/env python3
"""Public API Signature Stability Guard.

Compares AST signatures and defaults of public callables in modified files against
a base Git reference (default: HEAD~1 or origin/main) to prevent silent signature
mutilation, dropped parameters, inserted parameters, reordered arguments, or unintended default shifts.
"""

import ast
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def get_git_file_content(commit_ref: str, relative_path: str) -> str | None:
    """Retrieve file content from a specific git commit reference."""
    try:
        res = subprocess.run(
            ["git", "show", f"{commit_ref}:{relative_path}"],
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0:
            return res.stdout
    except Exception:
        pass
    return None


def get_changed_python_files(commit_ref: str, repo_root: Path) -> list[Path]:
    """Get list of changed .py files under molsysmt/ compared to commit_ref."""
    try:
        res = subprocess.run(
            ["git", "diff", "--name-only", commit_ref, "--", "molsysmt/"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        files = []
        for line in res.stdout.splitlines():
            line = line.strip()
            if line.endswith(".py") and (repo_root / line).exists():
                files.append(repo_root / line)
        return files
    except Exception:
        return []


def format_ast_default(node: ast.AST | None) -> str:
    """Convert an AST default node to a normalized string representation."""
    if node is None:
        return "<no_default>"
    try:
        return ast.unparse(node).strip()
    except Exception:
        return "<complex_expr>"


def extract_function_signatures(tree: ast.AST) -> dict[str, dict]:
    """Extract public function signatures and defaults from an AST."""
    signatures = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            # Only track public functions (not starting with _)
            if name.startswith("_"):
                continue

            args = node.args
            pos_args = [a.arg for a in args.args]
            kwonly_args = [a.arg for a in args.kwonlyargs]
            vararg = args.vararg.arg if args.vararg else None
            kwarg = args.kwarg.arg if args.kwarg else None

            # Map defaults to positional args
            n_pos = len(pos_args)
            n_defaults = len(args.defaults)
            pos_defaults = {}
            for i, d in enumerate(args.defaults):
                arg_name = pos_args[n_pos - n_defaults + i]
                pos_defaults[arg_name] = format_ast_default(d)

            # Map kwonly defaults
            kwonly_defaults = {}
            for a, d in zip(kwonly_args, args.kw_defaults):
                if d is not None:
                    kwonly_defaults[a] = format_ast_default(d)

            signatures[name] = {
                "lineno": node.lineno,
                "pos_args": pos_args,
                "pos_defaults": pos_defaults,
                "kwonly_args": kwonly_args,
                "kwonly_defaults": kwonly_defaults,
                "vararg": vararg,
                "kwarg": kwarg,
            }

    return signatures


def normalize_default_repr(val_str: str) -> str:
    """Normalize default value string representation for literal comparison without type coercion."""
    if val_str == "<no_default>":
        return val_str
    try:
        val = ast.literal_eval(val_str)
        return repr(val)
    except Exception:
        return val_str.strip()


def compare_signatures(old_sig: dict, new_sig: dict, func_name: str) -> list[str]:
    """Compare two function signatures and report any discrepancies."""
    violations = []

    old_pos = old_sig["pos_args"]
    new_pos = new_sig["pos_args"]

    # 1. Exact positional sequence check:
    if old_pos != new_pos:
        # Check dropped parameters
        for arg in old_pos:
            if arg not in new_pos and arg not in new_sig["kwonly_args"]:
                violations.append(f"Dropped positional parameter '{arg}' in function '{func_name}'")

        # Check parameter insertion or reordering
        if new_pos[: len(old_pos)] != old_pos:
            violations.append(
                f"Positional parameters altered (inserted/reordered) in '{func_name}': {old_pos} -> {new_pos}"
            )
        elif len(new_pos) > len(old_pos):
            added_args = new_pos[len(old_pos) :]
            violations.append(
                f"Added positional parameter(s) {added_args} in function '{func_name}'"
            )

    # 2. Keyword-only parameter checks
    old_kwonly = old_sig["kwonly_args"]
    new_kwonly = new_sig["kwonly_args"]
    for arg in old_kwonly:
        if arg not in new_kwonly and arg not in new_pos:
            violations.append(f"Dropped keyword-only parameter '{arg}' in function '{func_name}'")
    for arg in new_kwonly:
        if arg not in old_kwonly and arg not in old_pos:
            violations.append(f"Added keyword-only parameter '{arg}' in function '{func_name}'")

    # 3. Varargs / kwargs checks
    if old_sig["vararg"] != new_sig["vararg"]:
        violations.append(f"Vararg changed in '{func_name}': *{old_sig['vararg']} -> *{new_sig['vararg']}")
    if old_sig["kwarg"] != new_sig["kwarg"]:
        violations.append(f"Kwarg changed in '{func_name}': **{old_sig['kwarg']} -> **{new_sig['kwarg']}")

    # 4. Defaults checks (strictly preserving literal types e.g. list vs tuple)
    for arg, old_def in old_sig["pos_defaults"].items():
        if arg in new_sig["pos_defaults"]:
            new_def = new_sig["pos_defaults"][arg]
            if normalize_default_repr(old_def) != normalize_default_repr(new_def):
                violations.append(
                    f"Default value changed for '{arg}' in '{func_name}': {old_def} -> {new_def}"
                )
        elif arg in new_pos:
            violations.append(
                f"Default value removed for '{arg}' in '{func_name}': was {old_def}"
            )

    for arg, old_def in old_sig["kwonly_defaults"].items():
        if arg in new_sig["kwonly_defaults"]:
            new_def = new_sig["kwonly_defaults"][arg]
            if normalize_default_repr(old_def) != normalize_default_repr(new_def):
                violations.append(
                    f"Keyword-only default value changed for '{arg}' in '{func_name}': {old_def} -> {new_def}"
                )
        elif arg in new_kwonly:
            violations.append(
                f"Keyword-only default value removed for '{arg}' in '{func_name}': was {old_def}"
            )

    return violations


def load_signature_waivers(repo_root: Path) -> dict[str, str]:
    """Load declared intentional signature change waivers from public_api_stability.json."""
    json_path = repo_root / "devtools" / "data" / "public_api_stability.json"
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("signature_waivers", {})
        except Exception:
            pass
    return {}


def is_waiver_matched(rel_path: str, func_name: str, waivers: dict[str, str]) -> tuple[bool, str]:
    """Check if a file/function change has an explicit registered waiver."""
    candidates = [
        f"{rel_path}:{func_name}",
        rel_path,
        func_name,
    ]
    for c in candidates:
        if c in waivers:
            return True, waivers[c]
    return False, ""


def validate_api_stability(
    base_ref: str = "HEAD~1", repo_root: Path | None = None
) -> tuple[int, list[str]]:
    """Validate that no public API signature in modified files underwent unintended drift."""
    if repo_root is None:
        repo_root = Path(__file__).resolve().parent.parent.parent

    changed_files = get_changed_python_files(base_ref, repo_root)
    if not changed_files:
        return 0, [f"No modified Python files detected under molsysmt/ compared to {base_ref}."]

    waivers = load_signature_waivers(repo_root)
    all_violations = []
    waived_count = 0

    for file_path in changed_files:
        rel_path = file_path.relative_to(repo_root).as_posix()
        old_content = get_git_file_content(base_ref, rel_path)
        if old_content is None:
            # Newly added file, no regression against parent
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                new_content = f.read()
            old_tree = ast.parse(old_content, filename=rel_path)
            new_tree = ast.parse(new_content, filename=rel_path)
        except SyntaxError:
            continue

        old_sigs = extract_function_signatures(old_tree)
        new_sigs = extract_function_signatures(new_tree)

        for func_name, old_sig in old_sigs.items():
            waived, reason = is_waiver_matched(rel_path, func_name, waivers)

            if func_name not in new_sigs:
                if waived:
                    waived_count += 1
                else:
                    all_violations.append(
                        f"{rel_path}: Public function '{func_name}' was removed or renamed."
                    )
                continue

            diffs = compare_signatures(old_sig, new_sigs[func_name], func_name)
            if diffs:
                if waived:
                    waived_count += 1
                else:
                    for d in diffs:
                        all_violations.append(f"{rel_path}: {d}")

    status = 1 if all_violations else 0
    messages = all_violations
    if waived_count > 0:
        messages.append(f"Note: {waived_count} intentional signature modification(s) approved via signature_waivers registry.")

    return status, messages


def main():
    parser = argparse.ArgumentParser(
        description="Public API Signature Stability Guard against parent commit."
    )
    parser.add_argument(
        "--base",
        default="HEAD~1",
        help="Git commit/ref to compare against (default: HEAD~1)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent
    status, messages = validate_api_stability(base_ref=args.base, repo_root=repo_root)

    if status != 0:
        print(f"❌ Public API Stability Guard: {len(messages)} violation(s) detected:")
        for msg in messages:
            print(f"  - {msg}")
        sys.exit(1)
    else:
        print("✅ Public API Stability Guard: 0 unauthorized signature drifts detected.")
        for msg in messages:
            print(f"  {msg}")
        sys.exit(0)


if __name__ == "__main__":
    main()
