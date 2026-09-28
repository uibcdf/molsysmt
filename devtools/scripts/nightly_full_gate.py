#!/usr/bin/env python3
"""Run full nightly CI while skipped commits lack a successful full test run.

The last successful *executed* full Linux matrix is the watermark. A missed
schedule or failed matrix leaves skipped commits in the backlog for the next
night. API or history uncertainty makes the decision run the suite.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

SKIP_MARKER = re.compile(
    r"\[(?:skip ci|ci skip|no ci|skip actions|actions skip)\]"
    r"|^skip-checks:\s*true\s*$",
    re.IGNORECASE | re.MULTILINE,
)
FULL_VERSIONS = {"3.11", "3.12", "3.13"}


def api_json(path: str, token: str) -> dict:
    request = Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "molsysmt-nightly-full-gate",
        },
    )
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], text=True, capture_output=True, check=False
    )


def is_ancestor(commit: str, head: str) -> bool:
    return git("merge-base", "--is-ancestor", commit, head).returncode == 0


def full_matrix_passed(repository: str, run_id: int, token: str) -> bool:
    jobs = api_json(
        f"/repos/{repository}/actions/runs/{run_id}/jobs?per_page=100", token
    )["jobs"]
    passed = set()
    for job in jobs:
        match = re.fullmatch(r"Full test — ubuntu-latest, Python (3\.1[123])", job["name"])
        if not match or job["conclusion"] != "success":
            continue
        if any(
            step["name"] == "Run full test suite with coverage"
            and step["conclusion"] == "success"
            for step in job["steps"]
        ):
            passed.add(match.group(1))
    return passed == FULL_VERSIONS


def last_full_success(repository: str, head: str, token: str) -> str | None:
    for page in range(1, 4):
        data = api_json(
            f"/repos/{repository}/actions/workflows/ci-weekly.yaml/runs"
            f"?branch=main&status=success&per_page=100&page={page}",
            token,
        )
        runs = data["workflow_runs"]
        for run in runs:
            if run["event"] not in {"schedule", "workflow_dispatch"}:
                continue
            commit = run["head_sha"]
            if is_ancestor(commit, head) and full_matrix_passed(
                repository, run["id"], token
            ):
                return commit
        if len(runs) < 100:
            break
    return None


def skipped_commits_after(anchor: str, head: str) -> list[str]:
    revision = f"{anchor}..{head}" if anchor else head
    result = git("log", "-z", "--format=%H%x00%B", revision)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git log failed")
    fields = result.stdout.split("\x00")
    if fields[-1] != "":
        raise RuntimeError("incomplete git log output")
    return [
        fields[index]
        for index in range(0, len(fields) - 1, 2)
        if SKIP_MARKER.search(fields[index + 1])
    ]


def main() -> int:
    repository = os.environ["GITHUB_REPOSITORY"]
    head = os.environ["GITHUB_SHA"]
    token = os.environ["GITHUB_TOKEN"]
    try:
        anchor = last_full_success(repository, head, token)
        skipped = skipped_commits_after(anchor or "", head)
        run_full = anchor is None or bool(skipped)
        reason = (
            "no prior successful full matrix"
            if anchor is None
            else f"{len(skipped)} skipped commit(s) since full matrix {anchor}"
        )
    except (KeyError, OSError, URLError, RuntimeError, ValueError) as exc:
        anchor = None
        skipped = []
        run_full = True
        reason = f"cannot establish a clean backlog ({exc}); running full matrix"

    print(f"Nightly full CI: {'run' if run_full else 'skip'}; {reason}")
    if skipped:
        print("Skipped commits:", ", ".join(skipped))
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with Path(output).open("a", encoding="utf-8") as stream:
            stream.write(f"run_full={str(run_full).lower()}\n")
            stream.write(f"anchor={anchor or ''}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
