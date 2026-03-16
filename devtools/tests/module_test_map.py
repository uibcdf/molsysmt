from __future__ import annotations
import argparse
from pathlib import Path
from coverage_utils import dump_json, load_json

EXCLUDED_DIR_NAMES = {"__pycache__", ".pytest_cache"}

def module_name_from_path(path: Path, package_root_name: str) -> str:
    parts = list(path.parts)
    idx = parts.index(package_root_name)
    relevant = parts[idx:]
    out = []
    for part in relevant:
        if part.endswith(".py"):
            if part == "__init__.py":
                continue
            out.append(part[:-3])
        else:
            out.append(part)
    return ".".join(out)

def discover_modules(package_root: Path) -> list[dict]:
    package_root_name = package_root.name
    modules = []
    for path in package_root.rglob("*.py"):
        if any(p in EXCLUDED_DIR_NAMES for p in path.parts):
            continue
        module = module_name_from_path(path, package_root_name)
        modules.append({
            "module": module,
            "path": str(path),
            "parts": module.split("."),
        })
    modules.sort(key=lambda x: x["module"])
    return modules

def discover_tests(tests_root: Path) -> list[dict]:
    tests = []
    for path in list(tests_root.rglob("*.py")):
        if any(p in EXCLUDED_DIR_NAMES for p in path.parts):
            continue
        rel = path.relative_to(tests_root)
        tests.append({
            "path": str(path),
            "relative": str(rel),
            "parts": list(rel.parts),
            "stem": path.stem,
        })
    for path in [p for p in tests_root.rglob("*") if p.is_dir()]:
        if any(pn in EXCLUDED_DIR_NAMES for pn in path.parts):
            continue
        rel = path.relative_to(tests_root)
        tests.append({
            "path": str(path),
            "relative": str(rel),
            "parts": list(rel.parts),
            "stem": path.name,
        })
    return tests

def score_match(module_parts: list[str], test_parts: list[str], stem: str) -> int:
    score = 0
    mset = set(module_parts[1:]) if len(module_parts) > 1 else set(module_parts)
    tset = set([p.replace(".py", "") for p in test_parts] + [stem])
    overlap = mset & tset
    score += 10 * len(overlap)

    if len(module_parts) > 1 and module_parts[1] in tset:
        score += 15
    if module_parts[-1] in tset:
        score += 20

    joined = "/".join(test_parts)
    dotted = ".".join(module_parts[1:])
    if dotted and dotted.replace(".", "/") in joined:
        score += 25
    return score

def build_map(package_root: Path, tests_root: Path) -> dict:
    modules = discover_modules(package_root)
    tests = discover_tests(tests_root)
    package_root_name = package_root.name

    out = {
        "package_root": str(package_root),
        "tests_root": str(tests_root),
        "modules": [],
    }

    for mod in modules:
        candidates = []
        for test in tests:
            s = score_match(mod["parts"], test["parts"], test["stem"])
            if s > 0:
                candidates.append({
                    "score": s,
                    "path": test["path"],
                    "relative": test["relative"],
                })
        candidates.sort(key=lambda x: (-x["score"], x["relative"]))

        matched = [c for c in candidates if c["score"] >= 20]
        out["modules"].append({
            "module": mod["module"],
            "path": mod["path"],
            "associated_tests": matched[:20],
            "has_associated_tests": len(matched) > 0,
        })

    return out

def report_gaps(input_path: str):
    data = load_json(input_path)
    modules = data.get("modules", [])
    gaps = [m for m in modules if not m.get("has_associated_tests", False)]

    print("\nModules without associated tests (heuristic)\n")
    print(f"{'Module':<60}  Path")
    print("-" * 120)
    for item in gaps:
        print(f"{item['module']:<60}  {item['path']}")
    print(f"\nTotal modules without associated tests: {len(gaps)}")

def main():
    parser = argparse.ArgumentParser(description="Generate module/test association map or report gaps.")
    sub = parser.add_subparsers(dest="command")

    default_parser = argparse.ArgumentParser(add_help=False)
    default_parser.add_argument("--package-root")
    default_parser.add_argument("--tests-root")
    default_parser.add_argument("--output", default="module_test_map.json")

    gap_parser = sub.add_parser("report-gaps")
    gap_parser.add_argument("--input", required=True)

    args, unknown = parser.parse_known_args()

    if args.command == "report-gaps":
        report_gaps(args.input)
        return

    ap = argparse.ArgumentParser(description="Generate module/test association map.")
    ap.add_argument("--package-root", required=True)
    ap.add_argument("--tests-root", required=True)
    ap.add_argument("--output", default="module_test_map.json")
    opts = ap.parse_args()

    package_root = Path(opts.package_root).resolve()
    tests_root = Path(opts.tests_root).resolve()
    data = build_map(package_root, tests_root)
    dump_json(opts.output, data)
    print(f"Module/test map written to {opts.output}")

if __name__ == "__main__":
    main()
