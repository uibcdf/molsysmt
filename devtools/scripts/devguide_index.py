#!/usr/bin/env python3
"""Rendering the generated index of each developer-guide work queue.

Each queue `README.md` keeps a hand-written head -- how to read the directory, what
precedence it carries -- and a generated block between markers:

    <!-- generated: devguide_index -->
    <!-- /generated -->

The head is judgement and is written. The block is data and is rendered from the front
matter of the entries themselves, because `devguide/DOCUMENT_POLICY.md` forbids keeping
two manually independent authoritative lists, and an index of documents that already
describe themselves is exactly that.

Usage:
    python devtools/scripts/devguide_index.py            # write
    python devtools/scripts/devguide_index.py --check    # fail if stale
"""

from __future__ import annotations

import argparse
import sys

try:  # imported as devtools.scripts.devguide_index by the tests
    from devtools.scripts.devguide_reports import (
        CLOSED_STATUSES,
        DEVGUIDE_ROOT,
        OPEN_STATUSES,
        SEVERITIES,
        Report,
        load_queue,
        queue_directories,
    )
except ImportError:  # run as a script, with devtools/scripts on the path
    from devguide_reports import (
        CLOSED_STATUSES,
        DEVGUIDE_ROOT,
        OPEN_STATUSES,
        SEVERITIES,
        Report,
        load_queue,
        queue_directories,
    )


OPEN_MARKER = "<!-- generated: devguide_index -->"
CLOSE_MARKER = "<!-- /generated -->"

HEADINGS = {
    "open": "Open",
    "active": "In progress",
    "blocked": "Blocked",
    "partial": "Partially resolved",
    "resolved": "Resolved",
    "withdrawn": "Withdrawn",
    "superseded": "Superseded",
}

ISSUE_URL = "https://github.com/{owner_and_repository}/issues/{number}"


def _issue_link(report: Report) -> str:
    reference = report.issue
    number = report.issue_number
    if number is None:
        return "`no issue`"
    owner_and_repository = reference.rsplit("#", maxsplit=1)[0]
    url = ISSUE_URL.format(owner_and_repository=owner_and_repository, number=number)
    return f"[#{number}]({url})"


def _qualifiers(report: Report) -> str:
    parts = [str(report.get("severity"))] if report.get("severity") else []
    verification = report.get("verification")
    if verification:
        parts.append(str(verification))
    if report.is_archived and report.get("closed"):
        parts.append(f"closed {report.get('closed')}")
    return f" *({', '.join(parts)})*" if parts else ""


def _by_severity(report: Report) -> tuple[int, str]:
    """Worst first. Entries without a severity -- proposals -- sort after the graded ones."""

    severity = report.get("severity")
    rank = SEVERITIES.index(severity) if severity in SEVERITIES else len(SEVERITIES)
    return rank, report.path.name


def _entry(report: Report) -> str:
    name = report.path.name
    summary = report.summary or "*no summary*"
    blocked_by = report.get("blocked_by", [])
    line = f"- [`{name}`]({name}) — {_issue_link(report)} — {summary}{_qualifiers(report)}"
    if blocked_by:
        line += f"\n  Blocked by {', '.join(str(item) for item in blocked_by)}."
    return line


def render(reports: list[Report], archived: bool) -> str:
    """Render the block body for one queue."""

    if not reports:
        return "*No entries.*"

    order = CLOSED_STATUSES if archived else OPEN_STATUSES
    lines: list[str] = []

    for status in order:
        group = [report for report in reports if report.status == status]
        if not group:
            continue
        if archived:
            group.sort(
                key=lambda report: (str(report.get("closed", "")), report.path.name),
                reverse=True,
            )
        else:
            group.sort(key=_by_severity)
        lines.append(f"### {HEADINGS[status]} ({len(group)})")
        lines.append("")
        lines.extend(_entry(report) for report in group)
        lines.append("")

    unexpected = [report for report in reports if report.status not in order]
    if unexpected:
        lines.append("### Misfiled")
        lines.append("")
        lines.extend(_entry(report) for report in unexpected)
        lines.append("")

    return "\n".join(lines).rstrip()


def _replace_block(text: str, body: str) -> str:
    start = text.find(OPEN_MARKER)
    end = text.find(CLOSE_MARKER)
    if start == -1 or end == -1 or end < start:
        raise ValueError("markers missing")
    head = text[: start + len(OPEN_MARKER)]
    tail = text[end:]
    return f"{head}\n\n{body}\n\n{tail}"


def process(check: bool) -> tuple[list[str], list[str]]:
    """Returns the queues that changed (or are stale) and the errors found."""

    changed: list[str] = []
    errors: list[str] = []

    # Pending queues only. Archived directories predate this protocol, hold documents
    # without front matter, and are immutable under DOCUMENT_POLICY.md; the narrative
    # of a closed entry lives in that entry's own Resolution section.
    for queue in queue_directories(include_archives=False):
        directory = DEVGUIDE_ROOT / queue
        readme = directory / "README.md"
        if not directory.is_dir():
            continue
        if not readme.exists():
            errors.append(f"devguide/{queue}: no README.md to index")
            continue

        reports, queue_errors = load_queue(queue)
        errors.extend(queue_errors)

        text = readme.read_text(encoding="utf-8")
        body = render(reports, archived=queue.startswith("archive/"))
        try:
            updated = _replace_block(text, body)
        except ValueError:
            errors.append(
                f"devguide/{queue}/README.md: add the generated block markers\n"
                f"    {OPEN_MARKER}\n    {CLOSE_MARKER}"
            )
            continue

        if updated == text:
            continue
        changed.append(f"devguide/{queue}/README.md")
        if not check:
            readme.write_text(updated, encoding="utf-8")

    return changed, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit non-zero if any index is stale",
    )
    arguments = parser.parse_args()

    changed, errors = process(check=arguments.check)

    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    if arguments.check:
        for path in changed:
            print(f"stale: {path}", file=sys.stderr)
        if changed or errors:
            print(
                f"\n{len(changed)} stale index(es), {len(errors)} error(s). "
                f"Run: python devtools/scripts/devguide_index.py",
                file=sys.stderr,
            )
            return 1
        print("Every queue index is up to date.")
        return 0

    for path in changed:
        print(f"wrote: {path}")
    if not changed:
        print("Every queue index was already up to date.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
