from __future__ import annotations
import argparse, os
from coverage_utils import load_json

parser = argparse.ArgumentParser(description="Validate coverage thresholds.")
parser.add_argument("--summary-json", required=True)
parser.add_argument("--thresholds", required=True)
args = parser.parse_args()

if not os.path.exists(args.summary_json):
    raise SystemExit(f"Summary JSON not found: {args.summary_json}")
if not os.path.exists(args.thresholds):
    raise SystemExit(f"Thresholds file not found: {args.thresholds}")

summary = load_json(args.summary_json)
thresholds = load_json(args.thresholds)
overall_min = float(thresholds.get("overall_min_percent", 0.0))
overall = float(summary["overall"]["percent"])
failures = []

if overall < overall_min:
    failures.append(f"Overall coverage {overall:.1f}% is below threshold {overall_min:.1f}%")

packages = {row["package"]: row for row in summary.get("packages", [])}
for package_name, min_percent in thresholds.get("packages", {}).items():
    if package_name not in packages:
        failures.append(f"Threshold declared for {package_name}, but package was not found in summary output")
        continue
    percent = float(packages[package_name]["percent"])
    if percent < float(min_percent):
        failures.append(f"{package_name} coverage {percent:.1f}% is below threshold {float(min_percent):.1f}%")

print("\nCoverage threshold check\n")
print(f"Overall coverage: {overall:.1f}%")
print(f"Overall minimum:  {overall_min:.1f}%")
if thresholds.get("packages", {}):
    print("\nPackage thresholds:")
    for package_name, min_percent in thresholds["packages"].items():
        current = packages.get(package_name, {}).get("percent")
        current_s = "N/A" if current is None else f"{float(current):.1f}%"
        print(f"- {package_name}: current {current_s}, required {float(min_percent):.1f}%")

if failures:
    print("\nFAILED")
    for item in failures:
        print(f"- {item}")
    raise SystemExit(1)

print("\nPASSED")
