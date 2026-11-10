"""Report advisory timing observations only for established comparable inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import tempfile
from pathlib import Path

try:
    from .comparability import require_comparable
except ImportError:  # Direct CLI, including independent workflow receiving.
    from comparability import require_comparable


def _validated_results(data, label):
    """Require actual finite positive timing records before comparing ratios."""
    if not isinstance(data, dict):
        raise ValueError(f"{label} must be a JSON object.")
    results = data.get("results")
    if not isinstance(results, dict) or not results:
        raise ValueError(f"{label} must contain nonempty results.")
    for name, entry in results.items():
        if not isinstance(name, str) or not name.strip() or not isinstance(entry, dict):
            raise ValueError(f"{label} contains an invalid benchmark record.")
        value = entry.get("median_seconds")
        try:
            valid = (
                not isinstance(value, bool)
                and isinstance(value, (int, float))
                and math.isfinite(value)
                and value > 0
            )
        except OverflowError:
            valid = False
        if not valid:
            raise ValueError(
                f"{label} benchmark {name!r} requires finite positive median_seconds."
            )
    return results


def _write_report(path, report):
    """Publish a complete typed disposition without truncating a prior report."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent, delete=False
        ) as stream:
            temporary = Path(stream.name)
            json.dump(report, stream, indent=2, sort_keys=True, allow_nan=False)
            stream.write("\n")
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def compare_baselines(
    baseline_path: str, current_path: str, threshold: float = 0.15, *, report_path=None
) -> int:
    """Report comparable timing differences without restricting correct tools.

    Parameters
    ----------
    baseline_path : str
        Reference session JSON; this command never changes its bytes.
    current_path : str
        Current session JSON; this command never changes its bytes.
    threshold : float, default=0.15
        Advisory relative slowdown threshold, independent of API admission.
    report_path : str or None, default=None
        Optional machine-readable report, distinct from both input paths.

    Returns
    -------
    int
        Zero for a complete comparable observation, including warnings; one
        for unevaluable/partial evidence or a diagnostic publication failure.

    Notes
    -----
    Requires clean source identities, compatible recorded runtime/provider/
    resource/unit policies and identical input/observable/precision/measurement
    descriptions. Raw repeat samples must agree with their reported median.
    Legacy or incompatible sessions remain unevaluable. A matched protocol is
    not causal attribution or a statistical confidence claim. Repeated,
    comparable product inefficiency merits a reviewed improvement issue.
    """
    report = {
        "schema": "molsysmt.benchmark-comparison@1",
        "advisory": True,
        "verdict": "unevaluable",
        "comparable": False,
        "reasons": [],
        "comparisons": [],
        "unassessed_paths": [],
        "input_sha256": {},
    }
    if report_path is not None and Path(report_path).resolve() in {
        Path(baseline_path).resolve(),
        Path(current_path).resolve(),
    }:
        print("UNEVALUABLE: report destination must differ from both source sessions.")
        return 1

    def finish(code, reason=None):
        if reason is not None:
            report["reasons"].append(reason)
            print(f"UNEVALUABLE: {reason}")
        if report_path is not None:
            try:
                _write_report(report_path, report)
            except (OSError, TypeError, ValueError) as error:
                print(f"Diagnostic report publication failed: {error}")
                return 1
        return code

    try:
        data = []
        for label, path in [("Reference", baseline_path), ("Current", current_path)]:
            raw = Path(path).read_bytes()
            data.append(json.loads(raw))
            report["input_sha256"][label.lower()] = hashlib.sha256(raw).hexdigest()
        baseline, current = data
        if (
            isinstance(threshold, bool)
            or not isinstance(threshold, (int, float))
            or not math.isfinite(threshold)
            or threshold < 0
        ):
            raise ValueError("The threshold must be finite and nonnegative.")
        report["threshold"] = threshold
        base_results = _validated_results(baseline, "Reference baseline")
        current_results = _validated_results(current, "Current run")
        missing = sorted(set(base_results) - set(current_results))
        if missing:
            raise ValueError(
                f"Current run is missing reference measurements: {missing}"
            )
        require_comparable(baseline, current, base_results, current_results)
        report["unassessed_paths"] = sorted(set(current_results) - set(base_results))
        for name in sorted(set(base_results) & set(current_results)):
            first, second = base_results[name], current_results[name]
            change = second["median_seconds"] / first["median_seconds"] - 1
            if not math.isfinite(change):
                raise ValueError(f"{name}: timing ratio is outside finite float range.")
            report["comparisons"].append(
                {
                    "name": name,
                    "provider": second["workload"]["route"]["provider"],
                    "reference_median_seconds": first["median_seconds"],
                    "current_median_seconds": second["median_seconds"],
                    "relative_change": change,
                    "slowdown_warning": change > threshold,
                    "consistent_in_observed_ranges": min(second["samples_seconds"])
                    / max(first["samples_seconds"])
                    - 1
                    > threshold,
                    "reference_samples_seconds": first["samples_seconds"],
                    "current_samples_seconds": second["samples_seconds"],
                }
            )
    except (OSError, ValueError, TypeError, OverflowError) as error:
        return finish(1, str(error))

    report["comparable"] = True
    warnings = [row for row in report["comparisons"] if row["slowdown_warning"]]
    report["verdict"] = "warning" if warnings else "observed_within_threshold"
    print(
        f"MOLSYSMT ADVISORY PERFORMANCE OBSERVATIONS | threshold {threshold * 100:.1f}%"
    )
    print("Recorded context/workload compatible; no statistical or causal attribution.")
    for row in report["comparisons"]:
        print(
            f"{row['name']}: {row['reference_median_seconds'] * 1e6:.2f} -> {row['current_median_seconds'] * 1e6:.2f} us, {row['relative_change'] * 100:+.2f}%"
        )
    if warnings:
        print("WARNING: TIMING DIFFERENCES EXCEED THE ADVISORY THRESHOLD.")
        print(
            "Confirm repeated comparable product inefficiency in an improvement issue; do not restrict a correct tool."
        )
    else:
        print("OBSERVATION: Matched recorded timings meet the advisory threshold.")
    if report["unassessed_paths"]:
        report["verdict"] = "partial"
        return finish(1, f"New paths have no reference: {report['unassessed_paths']}")
    return finish(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="Reference session JSON")
    parser.add_argument("--current", required=True, help="Current session JSON")
    parser.add_argument(
        "--threshold", type=float, default=0.15, help="Advisory slowdown ratio"
    )
    parser.add_argument("--report", help="Separate machine-readable disposition JSON")
    args = parser.parse_args()
    sys.exit(
        compare_baselines(
            args.baseline, args.current, args.threshold, report_path=args.report
        )
    )
