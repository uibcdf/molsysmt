"""Keep the full-history integrity gate executable without dropping validators."""

from pathlib import Path

import yaml


def test_full_history_devguide_job_has_bounded_budget_and_retains_integrity_gates():
    root = Path(__file__).resolve().parents[2]
    workflow = yaml.safe_load((root / ".github/workflows/ci-devguide.yaml").read_text())
    job = workflow["jobs"]["validate"]
    assert "if" not in job
    # Two exact-head checkouts exceeded five minutes before any validator ran (#536).
    assert 15 <= job["timeout-minutes"] <= 30
    assert not job.get("continue-on-error", False)
    steps = job["steps"]
    (checkout,) = [
        step for step in steps if step.get("uses", "").startswith("actions/checkout@")
    ]
    assert checkout["with"]["fetch-depth"] == 0
    required = {
        "python devtools/scripts/validate_devguide.py",
        "python devtools/scripts/validate_development_archives.py",
        "python devtools/scripts/validate_api_stability.py",
        "python devtools/scripts/validate_scientific_evidence.py",
    }
    found = set()
    for step in steps:
        if step.get("run", "").strip() in required:
            assert "if" not in step and not step.get("continue-on-error", False)
            found.add(step["run"].strip())
    assert found == required
    (baseline,) = [step for step in steps if "--baseline" in step.get("run", "")]
    assert "if" not in baseline and not baseline.get("continue-on-error", False)
    assert "github.event.before" in baseline["env"]["BASE_SHA"]
    assert "github.event.pull_request.base.sha" in baseline["env"]["BASE_SHA"]
    assert "validate_api_stability.py --baseline" in baseline["run"]
