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


def _git_state(repo_root: Path) -> tuple[str, bool | None]:
    """Return the checked-out commit and whether tracked source is dirty."""
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if revision.returncode != 0:
        return "unknown", None
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    dirty = bool(status.stdout.strip()) if status.returncode == 0 else None
    return revision.stdout.strip(), dirty


def execute_nodes(
    node_ids: list[str],
    *,
    repo_root: Path,
    receptor: str = "llm",
    certificate_path: Path | None = None,
    require_clean: bool = False,
) -> tuple[bool, dict]:
    """Execute registered nodes and return their certificate verdict and payload."""
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
    commit, tracked_source_dirty = _git_state(repo_root)
    release_eligible = tests_passed and tracked_source_dirty is False
    verdict = tests_passed and (not require_clean or release_eligible)
    certificate = {
        "schema_version": "molsysmt.scientific-evidence-execution@1",
        "verdict": "pass" if verdict else "fail",
        "commit": commit,
        "tracked_source_dirty": tracked_source_dirty,
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
        help="fail unless tracked source matches the named Git commit",
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
                "Development evidence only: tracked source differs from the named "
                "commit or this is not a Git checkout, so this certificate is not "
                "release-eligible."
            )
        return 0
    print(f"Scientific evidence execution certificate: FAIL — {summary}.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
