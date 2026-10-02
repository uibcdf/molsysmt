"""Publication requires a retained report and its actual main-branch producer."""

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from devtools.scripts import coverage_artifact as publisher


def metadata():
    run = {
        "id": 12,
        "repository": {"id": 1, "full_name": publisher.REPOSITORY},
        "head_repository": {"id": 1, "full_name": publisher.REPOSITORY},
        "path": publisher.WORKFLOW,
        "head_branch": "main",
        "event": "workflow_dispatch",
        "status": "completed",
        "conclusion": "failure",
        "head_sha": "a" * 40,
    }
    jobs = {
        "total_count": 1,
        "jobs": [
            {
                "name": publisher.JOB,
                "status": "completed",
                "conclusion": "failure",
                "steps": [
                    {
                        "name": "Run full test suite with coverage",
                        "conclusion": "failure",
                    },
                    {
                        "name": "Retain coverage and test results",
                        "conclusion": "success",
                    },
                ],
            }
        ],
    }
    artifacts = {
        "total_count": 1,
        "artifacts": [
            {
                "id": 7,
                "name": publisher.ARTIFACT,
                "expired": False,
                "workflow_run": {
                    "id": 12,
                    "repository_id": 1,
                    "head_repository_id": 1,
                    "head_branch": "main",
                    "head_sha": "a" * 40,
                },
            }
        ],
    }
    return run, jobs, artifacts


def fetcher(payloads):
    run, jobs, artifacts = payloads

    def fetch(path):
        if "/jobs?" in path:
            return jobs
        if "/artifacts?" in path:
            return artifacts
        return run

    return fetch


def test_failed_completed_suite_uses_original_source_not_publisher_head():
    result = publisher.select_source("12", fetch=fetcher(metadata()))
    assert result == {"run_id": "12", "source_sha": "a" * 40, "artifact_id": "7"}


@pytest.mark.parametrize(
    "field,value",
    [
        ("path", ".github/workflows/untrusted.yaml"),
        ("head_branch", "feature"),
        ("event", "pull_request"),
        ("status", "in_progress"),
        ("conclusion", "cancelled"),
        ("head_sha", "not-a-sha"),
        ("id", 99),
    ],
)
def test_foreign_unfinished_or_invalid_sources_cannot_publish(field, value):
    payloads = metadata()
    payloads[0][field] = value
    with pytest.raises(ValueError):
        publisher.select_source("12", fetch=fetcher(payloads))


def test_forked_head_cannot_publish():
    payloads = metadata()
    payloads[0]["head_repository"]["full_name"] = "external/molsysmt"
    with pytest.raises(ValueError):
        publisher.select_source("12", fetch=fetcher(payloads))


def test_own_downstream_publication_waits_for_finished_producer():
    payloads = metadata()
    payloads[0].update(status="in_progress", conclusion=None)
    assert publisher.select_source("12", fetch=fetcher(payloads), current_run_id="12")
    payloads[1]["jobs"][0]["status"] = "in_progress"
    with pytest.raises(ValueError):
        publisher.select_source("12", fetch=fetcher(payloads), current_run_id="12")


@pytest.mark.parametrize(
    "mutation", ["aborted", "expired", "mismatch", "missing", "duplicate"]
)
def test_missing_aborted_expired_or_ambiguous_reports_cannot_publish(mutation):
    payloads = metadata()
    if mutation == "aborted":
        payloads[1]["jobs"][0]["steps"][1]["conclusion"] = "skipped"
    elif mutation == "expired":
        payloads[2]["artifacts"][0]["expired"] = True
    elif mutation == "mismatch":
        payloads[2]["artifacts"][0]["workflow_run"]["head_sha"] = "b" * 40
    elif mutation == "missing":
        payloads[2]["artifacts"] = []
    else:
        payloads[2]["artifacts"].append(deepcopy(payloads[2]["artifacts"][0]))
    with pytest.raises(ValueError):
        publisher.select_source("12", fetch=fetcher(payloads))


@pytest.mark.parametrize("run_id", ["0", "-1", "12/../34", "12\n", "$(false)"])
def test_run_identifier_cannot_change_native_request(run_id):
    with pytest.raises(ValueError):
        publisher.select_source(
            run_id, fetch=lambda _: pytest.fail("invalid ID fetched")
        )


def test_xml_must_be_nonempty_and_have_real_counts(tmp_path):
    path = tmp_path / "coverage.xml"
    path.write_text(
        '<coverage lines-valid="2" lines-covered="1" branches-valid="0" '
        'branches-covered="0"><packages><class /></packages></coverage>'
    )
    report = publisher.inspect_xml(path)
    assert report["lines-covered"] == 1 and len(report["xml_sha256"]) == 64
    path.write_text(
        '<coverage lines-valid="1" lines-covered="2" branches-valid="0" '
        'branches-covered="0"><packages><class /></packages></coverage>'
    )
    with pytest.raises(ValueError):
        publisher.inspect_xml(path)


def test_retry_uploads_only_validated_xml_for_measured_commit():
    root = Path(__file__).resolve().parents[2]
    workflow = yaml.load(
        (root / ".github/workflows/ci-coverage-upload.yaml").read_text(),
        Loader=yaml.BaseLoader,
    )
    assert set(workflow["on"]) == {"workflow_dispatch", "workflow_call"}
    job = workflow["jobs"]["publish"]
    assert "github.ref == 'refs/heads/main'" in job["if"]
    steps = job["steps"]
    download = next(s for s in steps if s.get("name", "").startswith("Download only"))
    assert download["with"]["artifact-ids"] == "${{ steps.source.outputs.artifact_id }}"
    upload = next(
        s for s in steps if s.get("name") == "Upload the measured report to Codecov"
    )
    assert upload["with"]["override_commit"] == "${{ steps.source.outputs.source_sha }}"
    assert (
        upload["with"]["disable_search"] == upload["with"]["fail_ci_if_error"] == "true"
    )
    assert upload["with"]["use_oidc"] == "true"
    assert "token" not in upload["with"]
    assert "flags" not in upload["with"]
    assert workflow["permissions"]["id-token"] == "write"
    assert not any("pytest" in s.get("run", "") for s in steps)
