from __future__ import annotations
import argparse
from datetime import datetime, timezone
from coverage_utils import load_json, dump_json, file_rows, aggregate_by_package, markdown_table, bar, grade, global_summary, sort_packages

parser = argparse.ArgumentParser(description="Generate Markdown and JSON coverage summaries.")
parser.add_argument("--root", default="molsysmt")
parser.add_argument("--top", type=int, default=15)
parser.add_argument("--package-depth", type=int, default=1)
parser.add_argument("--output", default="coverage_summary.md")
parser.add_argument("--json-output", default="coverage_summary.json")
parser.add_argument("--subpackage", default=None)
args = parser.parse_args()

data = load_json("coverage.json")
rows = file_rows(data, package_root=args.root, subpackage=args.subpackage)
rows_sorted = sorted(rows, key=lambda x: (x["percent"], -x["statements"], x["path"]))
packages_top = sort_packages(aggregate_by_package(rows, root=args.root, depth=1), mode="coverage")
packages = sort_packages(aggregate_by_package(rows, root=args.root, depth=args.package_depth), mode="coverage")
overall = global_summary(rows)
generated = datetime.now(timezone.utc).isoformat()

package_rows_top = [[r["package"], f'{r["percent"]:.1f}%', bar(r["percent"], 10), grade(r["percent"]), str(r["files"]), str(r["statements"]), str(r["missing"])] for r in packages_top]
package_rows = [[r["package"], f'{r["percent"]:.1f}%', bar(r["percent"], 10), grade(r["percent"]), str(r["files"]), str(r["statements"]), str(r["missing"])] for r in packages]
hotspot_rows = [[r["path"], f'{r["percent"]:.1f}%', str(r["statements"]), str(r["missing"])] for r in rows_sorted[:args.top]]

content = []
content.append("# Coverage Summary\n")
content.append(f"- Generated: {generated}")
content.append(f"- Package root: `{args.root}`")
if args.subpackage:
    content.append(f"- Subpackage filter: `{args.subpackage}`")
content.append(f"- Global coverage: **{overall['percent']:.1f}%**")
content.append(f"- Total files: **{overall['files']}**")
content.append(f"- Total statements: **{overall['statements']}**")
content.append(f"- Missing lines: **{overall['missing']}**\n")
content.append("## Coverage by top-level package\n")
content.append(markdown_table(["Package", "Coverage", "Map", "Grade", "Files", "Statements", "Missing"], package_rows_top))
content.append("\n\n## Coverage by package\n")
content.append(markdown_table(["Package", "Coverage", "Map", "Grade", "Files", "Statements", "Missing"], package_rows))
content.append("\n\n## Lowest coverage files\n")
content.append(markdown_table(["File", "Coverage", "Statements", "Missing"], hotspot_rows))
content.append("")

with open(args.output, "w", encoding="utf-8") as f:
    f.write("\n".join(content))

summary = {
    "generated_at_utc": generated,
    "package_root": args.root,
    "subpackage_filter": args.subpackage,
    "overall": overall,
    "top_level_packages": packages_top,
    "package_depth": args.package_depth,
    "packages": packages,
    "hotspots_top": args.top,
    "hotspots": rows_sorted[:args.top],
}
dump_json(args.json_output, summary)

print(f"Markdown summary written to {args.output}")
print(f"JSON summary written to {args.json_output}")
