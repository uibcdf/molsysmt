"""Resolve trusted MolSysMT coverage artifacts for publication without running tests.

This local CI profile accepts the retained Python 3.13 report from ci-weekly.yaml
on main. Native GitHub metadata establishes ownership and source identity; the
publisher must check out that source and must never execute downloaded artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from xml.etree import ElementTree

REPOSITORY = "uibcdf/molsysmt"
WORKFLOW = ".github/workflows/ci-weekly.yaml"
ARTIFACT = "full-suite-coverage-py3.13"
JOB = "Full test — ubuntu-latest, Python 3.13"


def native_json(path: str) -> dict:
    """Read native metadata through gh's existing authenticated API client."""
    return json.loads(
        subprocess.check_output(["gh", "api", "--method", "GET", path], text=True)
    )


def select_source(run_id: str, *, fetch=native_json, current_run_id: str = "") -> dict:
    """Return exact-source publication coordinates or reject incomplete provenance.

    A completed failed suite is reportable when its retention step succeeded.
    Aborted suites lack that successful retained report. An in-progress workflow
    is allowed only for its own downstream publisher after the producer job ends.
    Results are bounded to 100 jobs/artifacts; ambiguous or unavailable metadata
    raises instead of publishing an assumed report.
    """
    if not re.fullmatch(r"[1-9][0-9]{0,19}", run_id):
        raise ValueError("source_run_id must be a positive decimal GitHub run ID")
    base = f"repos/{REPOSITORY}/actions/runs/{run_id}"
    run = fetch(base)
    repository = run.get("repository", {})
    head_repository = run.get("head_repository", {})
    if (
        run.get("id") != int(run_id)
        or repository.get("full_name") != REPOSITORY
        or head_repository.get("full_name") != REPOSITORY
        or run.get("path") != WORKFLOW
        or run.get("head_branch") != "main"
        or run.get("event") not in {"schedule", "workflow_dispatch"}
    ):
        raise ValueError("source must be the owning main-branch full Linux workflow")
    terminal = run.get("status") == "completed" and run.get("conclusion") in {
        "success",
        "failure",
    }
    downstream = run_id == current_run_id and run.get("status") == "in_progress"
    if not (terminal or downstream):
        raise ValueError(
            "source execution is not completed or an eligible downstream run"
        )
    sha = run.get("head_sha", "")
    if not re.fullmatch(r"[a-f0-9]{40}", sha):
        raise ValueError("source execution has no full commit SHA")
    jobs = fetch(f"{base}/jobs?per_page=100")
    if jobs.get("total_count", 101) > 100:
        raise ValueError("source job inventory exceeds this bounded profile")
    producers = [job for job in jobs["jobs"] if job.get("name") == JOB]
    if len(producers) != 1:
        raise ValueError("source must have exactly one Python 3.13 producer")
    producer = producers[0]
    steps = {step["name"]: step for step in producer.get("steps", [])}
    suite = steps.get("Run full test suite with coverage", {})
    retained = steps.get("Retain coverage and test results", {})
    if (
        producer.get("status") != "completed"
        or producer.get("conclusion") not in {"success", "failure"}
        or suite.get("conclusion") not in {"success", "failure"}
        or retained.get("conclusion") != "success"
    ):
        raise ValueError(
            "source lacks an executed suite and successful report retention"
        )
    artifacts = fetch(f"{base}/artifacts?per_page=100")
    if artifacts.get("total_count", 101) > 100:
        raise ValueError("source artifact inventory exceeds this bounded profile")
    matches = [item for item in artifacts["artifacts"] if item.get("name") == ARTIFACT]
    if len(matches) != 1:
        raise ValueError("source must have exactly one retained Python 3.13 report")
    artifact = matches[0]
    provenance = artifact.get("workflow_run", {})
    if (
        artifact.get("expired") is not False
        or not isinstance(artifact.get("id"), int)
        or artifact["id"] <= 0
        or provenance.get("id") != int(run_id)
        or provenance.get("head_sha") != sha
        or provenance.get("head_branch") != "main"
        or provenance.get("repository_id") != repository.get("id")
        or provenance.get("head_repository_id") != repository.get("id")
    ):
        raise ValueError("artifact is expired or does not match its owning execution")
    return {"run_id": run_id, "source_sha": sha, "artifact_id": str(artifact["id"])}


def inspect_xml(path: Path) -> dict:
    """Check that the downloaded report has nonempty, consistent Cobertura counts."""
    root = ElementTree.parse(path).getroot()
    if root.tag != "coverage" or not root.findall(".//class"):
        raise ValueError("downloaded XML is not a nonempty coverage report")
    counts = {
        name: int(root.attrib[name])
        for name in (
            "lines-valid",
            "lines-covered",
            "branches-valid",
            "branches-covered",
        )
    }
    if not (
        0 <= counts["lines-covered"] <= counts["lines-valid"]
        and counts["lines-valid"] > 0
    ):
        raise ValueError("coverage line counts are inconsistent")
    if not (0 <= counts["branches-covered"] <= counts["branches-valid"]):
        raise ValueError("coverage branch counts are inconsistent")
    return {**counts, "xml_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xml", type=Path)
    args = parser.parse_args()
    if os.environ.get("GITHUB_REPOSITORY") != REPOSITORY:
        raise ValueError("this publication profile belongs to uibcdf/molsysmt")
    if args.xml:
        result = inspect_xml(args.xml)
    else:
        result = select_source(
            os.environ["SOURCE_RUN_ID"], current_run_id=os.environ["GITHUB_RUN_ID"]
        )
    print(json.dumps(result, sort_keys=True))
    with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as stream:
        for key, value in result.items():
            stream.write(f"{key}={value}\n")


if __name__ == "__main__":
    main()
