from __future__ import annotations
import argparse, os, json

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize(files_dict):
    out = {}
    for path, info in files_dict.items():
        summary = info.get("summary", {})
        out[path] = {
            "percent": float(summary.get("percent_covered", 0.0)),
            "stmts": int(summary.get("num_statements", 0)),
            "miss": int(summary.get("missing_lines", 0)),
        }
    return out

parser = argparse.ArgumentParser(description="Compare two coverage JSON reports.")
parser.add_argument("--baseline", required=True)
parser.add_argument("--current", required=True)
parser.add_argument("--top", type=int, default=20)
args = parser.parse_args()

if not os.path.exists(args.baseline):
    raise SystemExit(f"Baseline not found: {args.baseline}\nCreate it first, for example: cp coverage.json {args.baseline}")
if not os.path.exists(args.current):
    raise SystemExit(f"Current report not found: {args.current}")

baseline = summarize(load(args.baseline).get("files", {}))
current = summarize(load(args.current).get("files", {}))
all_paths = sorted(set(baseline) | set(current))
changed = []

for path in all_paths:
    b = baseline.get(path)
    c = current.get(path)
    if b is None:
        changed.append((999.0, "NEW", path, None, c["percent"]))
    elif c is None:
        changed.append((-999.0, "REMOVED", path, b["percent"], None))
    else:
        delta = c["percent"] - b["percent"]
        if abs(delta) > 1e-9 or c["stmts"] != b["stmts"] or c["miss"] != b["miss"]:
            changed.append((delta, "CHANGED", path, b["percent"], c["percent"]))

changed.sort(key=lambda x: (x[0], x[2]))

print("\nCoverage diff\n")
print(f"{'Delta':>8}  {'Status':>8}  {'Old':>7}  {'New':>7}  File")
print("-" * 110)
for delta, status, path, old, new in changed[:args.top]:
    old_s = "-" if old is None else f"{old:5.1f}%"
    new_s = "-" if new is None else f"{new:5.1f}%"
    print(f"{delta:+7.1f}  {status:>8}  {old_s:>7}  {new_s:>7}  {path}")

if not changed:
    print("No differences found between reports.")
