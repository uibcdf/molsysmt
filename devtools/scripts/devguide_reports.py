#!/usr/bin/env python3
"""Front matter of the developer-guide work queues.

Shared by `validate_devguide.py`, `devguide_index.py` and `devguide_issue.py`, so the
schema in `devguide/reporting_protocol.md` is described in exactly one place.

The parser deliberately accepts a restricted subset of YAML -- `key:`, `key: scalar`
and `key: [a, b]` -- and refuses anything else. Two reasons: `ci-devguide.yaml` runs the
validator on a bare interpreter with no installed dependencies, so PyYAML is not
available there; and a report header that cannot nest stays machine-simple by
construction.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEVGUIDE_ROOT = REPOSITORY_ROOT / "devguide"
MIGRATION_BASELINE = REPOSITORY_ROOT / "devtools/data/devguide_migration_baseline.json"

BUG_QUEUES = ("pending_bugs", "pending_bugs/docs")
# `pending_proposals/course_review` is absent on purpose: it holds retrospective planning
# inputs, not reports, and `devguide/reporting_protocol.md` places it outside the protocol.
PROPOSAL_QUEUES = ("pending_proposals", "pending_proposals/docs")
BUG_ARCHIVES = ("archive/resolved_bugs", "archive/withdrawn_bugs")
PROPOSAL_ARCHIVES = ("archive/resolved_proposals", "archive/resolved_proposals/docs")

OPEN_STATUSES = ("open", "active", "blocked", "partial")
CLOSED_STATUSES = ("resolved", "withdrawn", "superseded")
STATUSES = OPEN_STATUSES + CLOSED_STATUSES

VERIFICATIONS = ("reproduced", "measured", "inspected", "upstream", "asserted")
SEVERITIES = ("critical", "high", "medium", "low")

REQUIRED_FIELDS = ("summary", "issue", "status", "opened", "verification", "area")
KNOWN_FIELDS = REQUIRED_FIELDS + (
    "closed",
    "severity",
    "guard",
    "normative",
    "blocked_by",
    "supersedes",
)

STATE_LABELS = {"active": "in-progress", "blocked": "blocked", "partial": "partial"}

ISSUE_REFERENCE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[1-9][0-9]*$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SCALAR_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):(.*)$")

FRONT_MATTER_FENCE = "---"


class FrontMatterError(ValueError):
    """A header that cannot be read as the restricted subset."""


def split_front_matter(text: str) -> tuple[str | None, str]:
    """Return the raw front matter block and the body that follows it."""

    if not text.startswith(FRONT_MATTER_FENCE + "\n"):
        return None, text
    end = text.find("\n" + FRONT_MATTER_FENCE, len(FRONT_MATTER_FENCE))
    if end == -1:
        raise FrontMatterError("front matter is opened but never closed")
    block = text[len(FRONT_MATTER_FENCE) + 1 : end + 1]
    remainder = text[end + len(FRONT_MATTER_FENCE) + 1 :]
    return block, remainder.lstrip("\n")


def parse_front_matter(block: str) -> dict[str, object]:
    """Parse the restricted subset into scalars, lists and `None` for empty values."""

    parsed: dict[str, object] = {}
    for number, line in enumerate(block.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line != line.lstrip():
            raise FrontMatterError(
                f"line {number}: indented lines are not supported; write "
                f"lists inline as [a, b]"
            )
        match = SCALAR_LINE.match(line)
        if match is None:
            raise FrontMatterError(f"line {number}: expected 'key: value', got {line!r}")
        key, raw = match.group(1), match.group(2).strip()
        if key in parsed:
            raise FrontMatterError(f"line {number}: {key!r} appears more than once")
        parsed[key] = _parse_value(raw, number)
    return parsed


def _parse_value(raw: str, number: int) -> object:
    if raw == "":
        return None
    if raw.startswith("["):
        if not raw.endswith("]"):
            raise FrontMatterError(f"line {number}: list is opened but never closed")
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
    return raw.strip("'\"")


def _relative(path: Path) -> Path:
    try:
        return path.relative_to(REPOSITORY_ROOT)
    except ValueError:  # a queue rooted elsewhere, as in the tests
        return path


@dataclass
class Report:
    """One entry of a work queue."""

    path: Path
    queue: str
    front_matter: dict[str, object] = field(default_factory=dict)

    @property
    def relative(self) -> Path:
        return _relative(self.path)

    @property
    def is_bug(self) -> bool:
        return self.queue in BUG_QUEUES + BUG_ARCHIVES

    @property
    def is_archived(self) -> bool:
        return self.queue.startswith("archive/")

    def get(self, key: str, default: object = None) -> object:
        value = self.front_matter.get(key, default)
        return default if value is None else value

    @property
    def status(self) -> str:
        return str(self.get("status", ""))

    @property
    def summary(self) -> str:
        return str(self.get("summary", ""))

    @property
    def issue(self) -> str:
        return str(self.get("issue", ""))

    @property
    def issue_number(self) -> int | None:
        reference = self.issue
        if not ISSUE_REFERENCE.match(reference):
            return None
        return int(reference.rsplit("#", maxsplit=1)[1])

    @property
    def areas(self) -> list[str]:
        value = self.get("area", [])
        return [str(item) for item in value] if isinstance(value, list) else [str(value)]

    @property
    def labels(self) -> list[str]:
        """Labels derived from the front matter, without the ones set by hand."""

        derived = list(self.areas)
        state = STATE_LABELS.get(self.status)
        if state is not None:
            derived.append(state)
        if self.is_bug and self.get("severity") == "critical":
            derived.append("scientific-integrity")
        return sorted(set(derived))


def queue_directories(include_archives: bool = False) -> tuple[str, ...]:
    queues = BUG_QUEUES + PROPOSAL_QUEUES
    if include_archives:
        queues = queues + BUG_ARCHIVES + PROPOSAL_ARCHIVES
    return queues


def awaiting_migration() -> set[str]:
    """Entries filed before this protocol and not yet given a header.

    The list may only shrink. A queue entry created from now on fails validation
    without front matter whatever this file says.
    """

    if not MIGRATION_BASELINE.exists():
        return set()
    payload = json.loads(MIGRATION_BASELINE.read_text(encoding="utf-8"))
    return set(payload.get("awaiting_front_matter", ()))


def load_queue(queue: str) -> tuple[list[Report], list[str]]:
    """Load one queue. Returns its reports and the errors found while reading them."""

    reports: list[Report] = []
    errors: list[str] = []
    awaiting = awaiting_migration()
    directory = DEVGUIDE_ROOT / queue

    if not directory.is_dir():
        return reports, errors

    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        relative = _relative(path)
        try:
            block, _ = split_front_matter(path.read_text(encoding="utf-8"))
        except FrontMatterError as error:
            errors.append(f"{relative}: {error}")
            continue
        if block is None:
            # Documents archived before this protocol was adopted carry no front
            # matter, and DOCUMENT_POLICY.md makes archived material immutable, so
            # they are not retrofitted. In a pending queue the header is required
            # unless the entry is recorded as awaiting migration.
            if not queue.startswith("archive/") and str(relative) not in awaiting:
                errors.append(
                    f"{relative}: no front matter; every queue entry needs one "
                    f"(see devguide/reporting_protocol.md)"
                )
            continue
        try:
            front_matter = parse_front_matter(block)
        except FrontMatterError as error:
            errors.append(f"{relative}: {error}")
            continue
        reports.append(Report(path=path, queue=queue, front_matter=front_matter))

    return reports, errors


def load_all(include_archives: bool = False) -> tuple[list[Report], list[str]]:
    reports: list[Report] = []
    errors: list[str] = []
    for queue in queue_directories(include_archives=include_archives):
        queue_reports, queue_errors = load_queue(queue)
        reports.extend(queue_reports)
        errors.extend(queue_errors)
    return reports, errors


def validate(report: Report) -> list[str]:
    """Check one report against the schema in `devguide/reporting_protocol.md`."""

    errors: list[str] = []
    where = report.relative
    front_matter = report.front_matter

    def complain(message: str) -> None:
        errors.append(f"{where}: {message}")

    for key in front_matter:
        if key not in KNOWN_FIELDS:
            complain(f"unknown front matter field {key!r}")

    for key in REQUIRED_FIELDS:
        if front_matter.get(key) in (None, "", []):
            complain(f"missing required front matter field {key!r}")

    status = report.status
    if status and status not in STATUSES:
        complain(f"status {status!r} is not one of {', '.join(STATUSES)}")

    verification = report.get("verification")
    if verification and verification not in VERIFICATIONS:
        complain(
            f"verification {verification!r} is not one of {', '.join(VERIFICATIONS)}"
        )

    issue = report.issue
    if issue and not ISSUE_REFERENCE.match(issue):
        complain(f"issue {issue!r} is not of the form owner/repository#number")

    for key in ("opened", "closed"):
        value = report.get(key)
        if value and not ISO_DATE.match(str(value)):
            complain(f"{key} {value!r} is not an ISO date")

    severity = report.get("severity")
    if report.is_bug:
        if not severity:
            complain("a bug needs a severity")
        elif severity not in SEVERITIES:
            complain(f"severity {severity!r} is not one of {', '.join(SEVERITIES)}")
    elif severity:
        complain("severity applies to bugs only")

    for key in ("blocked_by", "supersedes"):
        value = report.get(key, [])
        if not isinstance(value, list):
            complain(f"{key} must be a list of issue references")
            continue
        for reference in value:
            if not ISSUE_REFERENCE.match(str(reference)):
                complain(f"{key} entry {reference!r} is not owner/repository#number")

    errors.extend(_validate_lifecycle(report))
    return errors


def _validate_lifecycle(report: Report) -> list[str]:
    errors: list[str] = []
    where = report.relative
    status = report.status
    closed = report.get("closed")

    if status in CLOSED_STATUSES and not closed:
        errors.append(f"{where}: status {status!r} needs a closed date")
    if status in OPEN_STATUSES and closed:
        errors.append(f"{where}: status {status!r} must not carry a closed date")

    if status in OPEN_STATUSES and report.is_archived:
        errors.append(f"{where}: status {status!r} does not belong under archive/")
    if status in CLOSED_STATUSES and not report.is_archived:
        errors.append(
            f"{where}: status {status!r} belongs under archive/, not in a pending queue"
        )

    if status == "blocked" and not report.get("blocked_by", []):
        errors.append(f"{where}: status 'blocked' needs blocked_by to name what blocks it")

    if status == "resolved":
        guard = report.get("guard")
        normative = report.get("normative")
        if not guard and not normative:
            errors.append(
                f"{where}: a resolved entry names the test that fails if it returns "
                f"(guard) or the normative document that absorbed its rules (normative)"
            )
        if guard:
            errors.extend(_validate_guard(where, str(guard)))
        if normative:
            target = DEVGUIDE_ROOT / str(normative)
            if not target.exists():
                target = REPOSITORY_ROOT / str(normative)
            if not target.exists():
                errors.append(f"{where}: normative document {normative!r} does not exist")

    return errors


def _validate_guard(where: Path, guard: str) -> list[str]:
    """A guard names a test file, optionally with `::test_name`, and the file exists."""

    path_part = guard.split("::", maxsplit=1)[0]
    if not path_part.startswith(("tests/", "devtools/tests/", "rust/")):
        return [
            f"{where}: guard {guard!r} does not point into a test tree "
            f"(tests/, devtools/tests/ or rust/)"
        ]
    if not (REPOSITORY_ROOT / path_part).exists():
        return [f"{where}: guard {guard!r} names a file that does not exist"]
    return []


def validate_all(include_archives: bool = True) -> list[str]:
    reports, errors = load_all(include_archives=include_archives)

    for report in reports:
        errors.extend(validate(report))

    # The migration baseline records debt, so it must not outlive it.
    awaiting = awaiting_migration()
    for report in reports:
        if str(report.relative) in awaiting:
            errors.append(
                f"{report.relative}: has front matter but is still listed in "
                f"{MIGRATION_BASELINE.relative_to(REPOSITORY_ROOT)}; remove it there"
            )
    for entry in sorted(awaiting):
        if not (REPOSITORY_ROOT / entry).exists():
            errors.append(
                f"{entry}: listed as awaiting migration but no longer exists; "
                f"remove it from {MIGRATION_BASELINE.relative_to(REPOSITORY_ROOT)}"
            )

    seen: dict[str, Path] = {}
    for report in reports:
        issue = report.issue
        if not issue or not ISSUE_REFERENCE.match(issue):
            continue
        # A theme may hold several documents, so a repeated issue is only reported
        # when the documents disagree about its state.
        first = seen.get(issue)
        if first is None:
            seen[issue] = report.path
            continue
        first_report = next(item for item in reports if item.path == first)
        if first_report.status != report.status:
            errors.append(
                f"{report.relative}: shares {issue} with "
                f"{first_report.relative} but reports status "
                f"{report.status!r} against {first_report.status!r}"
            )

    return errors
