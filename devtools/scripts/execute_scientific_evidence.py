#!/usr/bin/env python
"""Executing every pytest node registered as scientific evidence.

The structural registry validator intentionally does not import or execute test
modules. This command is the complementary heavy gate: it invokes exactly the
registered nodes, rejects collection errors, failures, and skips, and records a
machine-readable certificate for the exact environment in which they ran.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree

try:
    from devtools.scripts.validate_scientific_evidence import (
        API_REGISTRY_PATH,
        REPO_ROOT,
        _read_json,
        read_evidence_registry,
        scientific_test_nodes,
        validate_registry,
    )
except ImportError:
    from validate_scientific_evidence import (
        API_REGISTRY_PATH,
        REPO_ROOT,
        _read_json,
        read_evidence_registry,
        scientific_test_nodes,
        validate_registry,
    )


def _junit_counts(path: Path) -> dict[str, int]:
    """Return aggregate pytest counts from one JUnit XML report."""
    root = ElementTree.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    return {
        field: sum(int(suite.attrib.get(field, 0)) for suite in suites)
        for field in ("tests", "failures", "errors", "skipped")
    }


WORKFLOW_OUTPUT_PATHS = frozenset(
    {
        "scientific-evidence-certificate.json",
        "junit.xml",
        "coverage.xml",
        ".pytest-receptor/events.jsonl",
    }
)


def _git_state(repo_root: Path) -> dict:
    """Capture nonignored source separately from reserved workflow outputs."""
    state = {
        "commit": "unknown",
        "tracked_source_dirty": None,
        "untracked_source_paths": None,
        "untracked_workflow_artifacts": None,
    }
    git = ["git", "-c", "core.fsmonitor=false"]
    revision = subprocess.run(
        [*git, "rev-parse", "--verify", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if revision.returncode != 0:
        return state
    state["commit"] = revision.stdout.strip()
    status = subprocess.run(
        [*git, "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if status.returncode != 0:
        return state
    dirty, inputs, artifacts = False, [], []
    records = iter(status.stdout.split(b"\0"))
    for record in records:
        if not record:
            continue
        code, path = record[:2], os.fsdecode(record[3:])
        if code == b"??":
            (artifacts if path in WORKFLOW_OUTPUT_PATHS else inputs).append(path)
        else:
            dirty = True
            if b"R" in code or b"C" in code:
                next(records, None)  # A rename/copy has a second NUL-delimited path.
    state.update(
        tracked_source_dirty=dirty,
        untracked_source_paths=sorted(inputs),
        untracked_workflow_artifacts=sorted(artifacts),
    )
    return state


def execute_nodes(
    node_ids: list[str],
    *,
    repo_root: Path,
    receptor: str = "llm",
    certificate_path: Path | None = None,
    require_clean: bool = False,
) -> tuple[bool, dict]:
    """Execute registered nodes and return their certificate verdict and payload."""
    source_before = _git_state(repo_root)
    with tempfile.TemporaryDirectory(prefix="molsysmt-scientific-evidence-") as tmp:
        junit_path = Path(tmp) / "junit.xml"
        command = [
            sys.executable,
            "-m",
            "pytest",
            "-p",
            "no:xdist",
            f"--receptor={receptor}",
            f"--junitxml={junit_path}",
            *node_ids,
        ]
        result = subprocess.run(command, cwd=repo_root, check=False)
        counts = (
            _junit_counts(junit_path)
            if junit_path.is_file()
            else {field: 0 for field in ("tests", "failures", "errors", "skipped")}
        )

    passed = counts["tests"] - sum(
        counts[field] for field in ("failures", "errors", "skipped")
    )
    tests_passed = (
        result.returncode == 0
        and counts["tests"] >= len(node_ids)
        and counts["failures"] == 0
        and counts["errors"] == 0
        and counts["skipped"] == 0
    )
    source_after = _git_state(repo_root)
    source_correspondence = (
        source_before["commit"] != "unknown"
        and source_before["commit"] == source_after["commit"]
        and all(
            source["tracked_source_dirty"] is False
            and source["untracked_source_paths"] == []
            for source in (source_before, source_after)
        )
    )
    release_eligible = tests_passed and source_correspondence
    verdict = tests_passed and (not require_clean or release_eligible)
    certificate = {
        "schema_version": "molsysmt.scientific-evidence-execution@1",
        "verdict": "pass" if verdict else "fail",
        "commit": source_after["commit"],
        "tracked_source_dirty": source_after["tracked_source_dirty"],
        "source_before": source_before,
        "source_after": source_after,
        "source_correspondence": source_correspondence,
        "release_eligible": release_eligible,
        "created_at": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "registered_nodes": len(node_ids),
        "collected_cases": counts["tests"],
        "passed": passed,
        "failures": counts["failures"],
        "errors": counts["errors"],
        "skipped": counts["skipped"],
        "pytest_exit_code": result.returncode,
        "nodes": node_ids,
    }
    if certificate_path is not None:
        certificate_path.parent.mkdir(parents=True, exist_ok=True)
        certificate_path.write_text(
            json.dumps(certificate, indent=2) + "\n", encoding="utf-8"
        )
    return verdict, certificate


def main(argv: list[str] | None = None) -> int:
    """Validate the registry, execute its nodes, and emit a certificate."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--receptor",
        choices=("llm", "ci", "human"),
        default="llm",
        help="pytest-receptor output mode (default: llm)",
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        help="optional path for the JSON execution certificate",
    )
    parser.add_argument(
        "--require-clean",
        action="store_true",
        help="fail unless source matches one known Git commit before and after execution",
    )
    args = parser.parse_args(argv)

    registry, load_errors = read_evidence_registry()
    errors = load_errors + validate_registry(
        registry, _read_json(API_REGISTRY_PATH), REPO_ROOT
    )
    if errors:
        print("Scientific evidence registry violations:")
        for error in errors:
            print(f"- {error}")
        return 1

    node_ids = scientific_test_nodes(registry)
    verdict, certificate = execute_nodes(
        node_ids,
        repo_root=REPO_ROOT,
        receptor=args.receptor,
        certificate_path=args.certificate,
        require_clean=args.require_clean,
    )
    summary = (
        f"{certificate['passed']}/{certificate['collected_cases']} cases passed for "
        f"{certificate['registered_nodes']} registered nodes; "
        f"{certificate['skipped']} skipped, {certificate['failures']} failed, "
        f"{certificate['errors']} errors"
    )
    if verdict:
        print(f"Scientific evidence execution certificate: PASS — {summary}.")
        if not certificate["release_eligible"]:
            print(
                "Development evidence only: source correspondence to one Git commit "
                "is not established. Inspect source_before/source_after; this "
                "certificate is not release-eligible."
            )
        return 0
    print(f"Scientific evidence execution certificate: FAIL — {summary}.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
