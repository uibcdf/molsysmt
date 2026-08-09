#!/usr/bin/env python3
"""Keeping the issue board and the developer-guide work queues in step.

The front matter of each entry is the single source; this script only pushes it to
GitHub. It never reads state back into a document, and it never writes analysis into an
issue: the protocol in `devguide/reporting_protocol.md` keeps the reasoning in the
document and leaves the issue holding state and settled facts.

Needs the network and an authenticated `gh`, so it is not part of the release gate.

Usage:
    devguide_issue.py open  --kind bug --title "..." --area form,convert [--severity high]
    devguide_issue.py sync  [--check]
    devguide_issue.py close devguide/pending_bugs/<file>.md --users "..." [--commit SHA]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:  # imported as devtools.scripts.devguide_issue by the tests
    from devtools.scripts.devguide_reports import (
        CLOSED_STATUSES,
        DEVGUIDE_ROOT,
        REPOSITORY_ROOT,
        Report,
        load_all,
        parse_front_matter,
        split_front_matter,
        validate,
    )
except ImportError:  # run as a script, with devtools/scripts on the path
    from devguide_reports import (
        CLOSED_STATUSES,
        DEVGUIDE_ROOT,
        REPOSITORY_ROOT,
        Report,
        load_all,
        parse_front_matter,
        split_front_matter,
        validate,
    )


KIND_LABELS = ("bug", "proposal", "enhancement", "documentation")
QUEUE_FOR_KIND = {
    "bug": "pending_bugs",
    "documentation": "pending_bugs/docs",
    "proposal": "pending_proposals",
    "enhancement": "pending_proposals",
}
MANAGED_LABELS = ("in-progress", "blocked", "partial")


def _gh(*arguments: str, capture: bool = True) -> str:
    result = subprocess.run(
        ("gh",) + arguments,
        capture_output=capture,
        text=True,
        cwd=REPOSITORY_ROOT,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        raise SystemExit(f"gh {' '.join(arguments)} failed: {message}")
    return (result.stdout or "").strip()


def _slug(title: str) -> str:
    kept = [character.lower() if character.isalnum() else "_" for character in title]
    slug = "".join(kept)
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug.strip("_")[:80]


def command_open(arguments: argparse.Namespace) -> int:
    """Create the issue, then scaffold the document with its number already in place."""

    areas = [area.strip() for area in arguments.area.split(",") if area.strip()]
    labels = [arguments.kind] + areas
    if arguments.severity == "critical":
        labels.append("scientific-integrity")

    body = (
        f"What  — {arguments.title}\n"
        f"How   — <the command that shows it, or how it would be done>\n"
        f"Why   — <impact, or the problem it solves>\n"
        f"Record — <filled in when the document lands>\n"
    )

    url = _gh(
        "issue",
        "create",
        "--title",
        arguments.title,
        "--body",
        body,
        "--label",
        ",".join(labels),
    ).splitlines()[-1]
    number = url.rsplit("/", maxsplit=1)[1]
    repository = _gh("repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner")

    queue = arguments.queue or QUEUE_FOR_KIND[arguments.kind]
    document = DEVGUIDE_ROOT / queue / f"{_slug(arguments.title)}.md"
    if document.exists():
        raise SystemExit(f"{document.relative_to(REPOSITORY_ROOT)} already exists")

    template = (DEVGUIDE_ROOT / "templates" / "report.md").read_text(encoding="utf-8")
    block, remainder = split_front_matter(template)
    assert block is not None
    filled = (
        block.replace("summary: One line, present tense. Becomes the issue title.",
                      f"summary: {arguments.title}")
        .replace("issue: uibcdf/molsysmt#000", f"issue: {repository}#{number}")
        .replace("opened: 2026-01-01", f"opened: {arguments.today}")
        .replace("area: []", f"area: [{', '.join(areas)}]")
    )
    if arguments.severity:
        filled = filled.replace("severity: medium", f"severity: {arguments.severity}")
    else:
        filled = "".join(
            line for line in filled.splitlines(keepends=True)
            if not line.startswith("severity:")
        )

    document.parent.mkdir(parents=True, exist_ok=True)
    document.write_text(f"---\n{filled}---\n\n{remainder}", encoding="utf-8")

    relative = document.relative_to(REPOSITORY_ROOT)
    print(f"issue:    {url}")
    print(f"document: {relative}")
    print(f"\nFill in the document, then update the issue's Record line to {relative}")
    return 0


def _remote_state() -> dict[int, dict]:
    payload = _gh(
        "issue", "list", "--state", "all", "--limit", "500",
        "--json", "number,state,labels,title",
    )
    issues = json.loads(payload or "[]")
    return {issue["number"]: issue for issue in issues}


def _drift(report: Report, issue: dict | None) -> list[str]:
    where = report.relative
    if issue is None:
        return [f"{where}: {report.issue} does not exist on the board"]

    problems: list[str] = []
    should_be_closed = report.status in CLOSED_STATUSES
    is_closed = issue["state"].upper() == "CLOSED"
    if should_be_closed and not is_closed:
        problems.append(f"{where}: status {report.status!r} but {report.issue} is open")
    if not should_be_closed and is_closed:
        problems.append(f"{where}: status {report.status!r} but {report.issue} is closed")

    present = {label["name"] for label in issue["labels"]}
    wanted = set(report.labels)
    managed = set(MANAGED_LABELS)
    stale = (present & managed) - wanted
    missing = wanted - present
    if stale:
        problems.append(f"{where}: {report.issue} carries stale labels {sorted(stale)}")
    if missing:
        problems.append(f"{where}: {report.issue} is missing labels {sorted(missing)}")
    return problems


def command_sync(arguments: argparse.Namespace) -> int:
    reports, errors = load_all(include_archives=True)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    remote = _remote_state()
    drifted = 0

    for report in reports:
        number = report.issue_number
        if number is None:
            continue
        issue = remote.get(number)
        problems = _drift(report, issue)
        if not problems:
            continue
        drifted += 1
        for problem in problems:
            print(problem)
        if arguments.check or issue is None:
            continue

        present = {label["name"] for label in issue["labels"]}
        wanted = set(report.labels)
        add = sorted(wanted - present)
        remove = sorted((present & set(MANAGED_LABELS)) - wanted)
        if add or remove:
            call = ["issue", "edit", str(number)]
            for label in add:
                call += ["--add-label", label]
            for label in remove:
                call += ["--remove-label", label]
            _gh(*call)
            print(f"  synchronised labels on #{number}")

    if arguments.check:
        print(f"\n{drifted} entr(ies) drifted." if drifted else "\nBoard agrees with the queues.")
        return 1 if (drifted or errors) else 0

    print(f"\n{drifted} entr(ies) needed synchronising.")
    return 1 if errors else 0


def command_close(arguments: argparse.Namespace) -> int:
    document = Path(arguments.document).resolve()
    if not document.exists():
        raise SystemExit(f"{arguments.document} does not exist")

    queue = str(document.parent.relative_to(DEVGUIDE_ROOT))
    block, _ = split_front_matter(document.read_text(encoding="utf-8"))
    if block is None:
        raise SystemExit(f"{arguments.document} has no front matter")

    report = Report(path=document, queue=queue, front_matter=parse_front_matter(block))

    problems = validate(report)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        raise SystemExit("the document does not satisfy the protocol yet")
    if report.status not in CLOSED_STATUSES:
        raise SystemExit(
            f"status is {report.status!r}; set it to one of "
            f"{', '.join(CLOSED_STATUSES)} and move the document under archive/ first"
        )

    commit = arguments.commit or _git("rev-parse", "--short", "HEAD")
    subject = _git("log", "-1", "--format=%s", commit)

    verdict = "Fixed in" if report.is_bug else "Decision —"
    lines = [f"{verdict} {commit} — {subject}", ""]
    lines.append(f"For users — {arguments.users}")
    if report.get("guard"):
        lines.append(f"Guard  — {report.get('guard')}")
    if report.get("normative"):
        lines.append(f"Rules  — {report.get('normative')}")
    lines.append(f"Record — {report.relative}")
    comment = "\n".join(lines)

    number = report.issue_number
    if number is None:
        raise SystemExit(f"{report.relative}: front matter has no usable issue")

    if arguments.dry_run:
        print(f"would close #{number} with:\n\n{comment}")
        return 0

    _gh("issue", "close", str(number), "--comment", comment)
    print(f"closed #{number}\n\n{comment}")
    return 0


def _git(*arguments: str) -> str:
    result = subprocess.run(
        ("git",) + arguments, capture_output=True, text=True, cwd=REPOSITORY_ROOT
    )
    if result.returncode != 0:
        raise SystemExit(f"git {' '.join(arguments)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    opener = subparsers.add_parser("open", help="create an issue and scaffold its document")
    opener.add_argument("--kind", required=True, choices=KIND_LABELS)
    opener.add_argument("--title", required=True)
    opener.add_argument("--area", required=True, help="comma-separated area labels")
    opener.add_argument("--severity", choices=("critical", "high", "medium", "low"))
    opener.add_argument("--queue", help="override the queue the document lands in")
    opener.add_argument("--today", default=None, help="ISO date, defaults to today")
    opener.set_defaults(handler=command_open)

    syncer = subparsers.add_parser("sync", help="push derived labels and state to the board")
    syncer.add_argument("--check", action="store_true", help="report drift, change nothing")
    syncer.set_defaults(handler=command_sync)

    closer = subparsers.add_parser("close", help="close the issue behind an archived document")
    closer.add_argument("document")
    closer.add_argument("--users", required=True, help="the 'For users' line")
    closer.add_argument("--commit", help="defaults to HEAD")
    closer.add_argument("--dry-run", action="store_true")
    closer.set_defaults(handler=command_close)

    arguments = parser.parse_args()
    if getattr(arguments, "today", "sentinel") is None:
        from datetime import date

        arguments.today = date.today().isoformat()
    return arguments.handler(arguments)


if __name__ == "__main__":
    sys.exit(main())
