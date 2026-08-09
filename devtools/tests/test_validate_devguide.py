"""Schema, lifecycle and index behaviour of the developer-guide work queues.

The protocol these enforce is `devguide/reporting_protocol.md`.
"""

from pathlib import Path

import pytest

from devtools.scripts import devguide_index, devguide_reports


VALID = {
    "summary": "A defect.",
    "issue": "uibcdf/molsysmt#137",
    "status": "open",
    "opened": "2026-08-09",
    "closed": None,
    "severity": "high",
    "verification": "reproduced",
    "area": ["form"],
    "guard": None,
    "normative": None,
    "blocked_by": [],
    "supersedes": [],
}


def _report(queue="pending_bugs", name="entry.md", **overrides):
    front_matter = dict(VALID)
    front_matter.update(overrides)
    path = devguide_reports.DEVGUIDE_ROOT / queue / name
    return devguide_reports.Report(path=path, queue=queue, front_matter=front_matter)


def _errors(**overrides):
    return devguide_reports.validate(_report(**overrides))


# --- the restricted front matter subset ------------------------------------------


def test_scalars_lists_and_empty_values_are_parsed():
    parsed = devguide_reports.parse_front_matter(
        "summary: One line\nclosed:\narea: [form, convert]\nblocked_by: []\n"
    )
    assert parsed == {
        "summary": "One line",
        "closed": None,
        "area": ["form", "convert"],
        "blocked_by": [],
    }


def test_the_body_survives_the_split():
    block, body = devguide_reports.split_front_matter("---\nsummary: x\n---\n\n# Title\n")
    assert block == "summary: x\n"
    assert body == "# Title\n"


def test_a_document_without_front_matter_is_reported_as_such():
    block, body = devguide_reports.split_front_matter("# Title\n")
    assert block is None
    assert body == "# Title\n"


@pytest.mark.parametrize(
    "block",
    [
        "summary: x\nnested:\n  key: value\n",   # indentation is not supported
        "summary: x\narea: [form\n",             # list never closed
        "this line has no colon\n",
        "summary: one\nsummary: two\n",          # duplicate key
    ],
)
def test_headers_outside_the_subset_are_refused(block):
    with pytest.raises(devguide_reports.FrontMatterError):
        devguide_reports.parse_front_matter(block)


def test_an_unterminated_header_is_refused():
    with pytest.raises(devguide_reports.FrontMatterError):
        devguide_reports.split_front_matter("---\nsummary: x\n")


# --- the schema -------------------------------------------------------------------


def test_a_well_formed_entry_passes():
    assert _errors() == []


@pytest.mark.parametrize("field", devguide_reports.REQUIRED_FIELDS)
def test_every_required_field_is_required(field):
    errors = _errors(**{field: None})
    assert any(f"missing required front matter field {field!r}" in e for e in errors)


def test_an_unknown_field_is_refused():
    assert any("unknown front matter field" in e for e in _errors(priority="urgent"))


def test_the_vocabularies_are_closed():
    assert any("status 'wip'" in e for e in _errors(status="wip"))
    assert any("verification 'guessed'" in e for e in _errors(verification="guessed"))
    assert any("severity 'urgent'" in e for e in _errors(severity="urgent"))


def test_an_issue_reference_names_owner_repository_and_number():
    assert any("is not of the form" in e for e in _errors(issue="molsysmt#12"))
    assert any("is not of the form" in e for e in _errors(issue="uibcdf/molsysmt"))
    assert _errors(issue="uibcdf/smonitor#4") == []


def test_dates_are_iso():
    assert any("is not an ISO date" in e for e in _errors(opened="9 August 2026"))


def test_severity_belongs_to_bugs_only():
    assert any("a bug needs a severity" in e for e in _errors(severity=None))
    errors = _errors(queue="pending_proposals", severity="high")
    assert any("severity applies to bugs only" in e for e in errors)


def test_blocked_by_holds_issue_references_not_prose():
    errors = _errors(blocked_by=["waiting for upstream"])
    assert any("is not owner/repository#number" in e for e in errors)


# --- the lifecycle ----------------------------------------------------------------


def test_a_closed_status_needs_a_closed_date():
    errors = _errors(
        queue="archive/resolved_bugs", status="withdrawn", closed=None
    )
    assert any("needs a closed date" in e for e in errors)


def test_an_open_status_must_not_carry_a_closed_date():
    assert any("must not carry a closed date" in e for e in _errors(closed="2026-08-09"))


def test_a_closed_entry_belongs_under_archive():
    errors = _errors(status="withdrawn", closed="2026-08-09")
    assert any("belongs under archive/" in e for e in errors)


def test_an_open_entry_does_not_belong_under_archive():
    errors = _errors(queue="archive/resolved_bugs", status="open")
    assert any("does not belong under archive/" in e for e in errors)


def test_blocked_names_what_blocks_it():
    errors = _errors(status="blocked", blocked_by=[])
    assert any("needs blocked_by" in e for e in errors)


def test_resolved_without_a_guard_or_a_normative_document_is_refused():
    errors = _errors(
        queue="archive/resolved_bugs", status="resolved", closed="2026-08-09"
    )
    assert any("names the test that fails if it returns" in e for e in errors)


def test_a_guard_must_point_at_a_file_that_exists():
    errors = _errors(
        queue="archive/resolved_bugs",
        status="resolved",
        closed="2026-08-09",
        guard="tests/does_not_exist.py::test_nothing",
    )
    assert any("names a file that does not exist" in e for e in errors)


def test_a_guard_outside_the_test_tree_is_refused():
    errors = _errors(
        queue="archive/resolved_bugs",
        status="resolved",
        closed="2026-08-09",
        guard="molsysmt/basic/get_form.py",
    )
    assert any("does not point into a test tree" in e for e in errors)


def test_a_real_guard_is_accepted():
    guard = "tests/basic/test_get_form_battery.py"
    assert (devguide_reports.REPOSITORY_ROOT / guard).exists(), "fixture moved"
    errors = _errors(
        queue="archive/resolved_bugs",
        status="resolved",
        closed="2026-08-09",
        guard=f"{guard}::test_routes",
    )
    assert errors == []


def test_a_proposal_may_close_on_a_normative_document_instead():
    errors = _errors(
        queue="archive/resolved_proposals",
        status="resolved",
        closed="2026-08-09",
        severity=None,
        normative="DOCUMENT_POLICY.md",
    )
    assert errors == []


# --- derived labels ---------------------------------------------------------------


def test_areas_and_state_become_labels():
    report = _report(status="active", area=["form", "convert"])
    assert report.labels == ["convert", "form", "in-progress"]


def test_an_untouched_entry_carries_no_state_label():
    assert _report(status="open").labels == ["form"]


def test_only_a_critical_bug_is_promoted_to_scientific_integrity():
    assert "scientific-integrity" in _report(severity="critical").labels
    assert "scientific-integrity" not in _report(severity="high").labels


# --- loading and indexing ---------------------------------------------------------


def _queue(tmp_path, monkeypatch, name, documents):
    directory = tmp_path / name
    directory.mkdir(parents=True)
    for filename, text in documents.items():
        (directory / filename).write_text(text, encoding="utf-8")
    monkeypatch.setattr(devguide_reports, "DEVGUIDE_ROOT", tmp_path)
    monkeypatch.setattr(devguide_index, "DEVGUIDE_ROOT", tmp_path)
    return directory


def test_a_pending_entry_without_front_matter_is_an_error(tmp_path, monkeypatch):
    _queue(tmp_path, monkeypatch, "pending_bugs", {"a.md": "# No header\n"})
    _, errors = devguide_reports.load_queue("pending_bugs")
    assert any("no front matter" in error for error in errors)


def test_archived_documents_predating_the_protocol_are_left_alone(tmp_path, monkeypatch):
    _queue(tmp_path, monkeypatch, "archive/resolved_bugs", {"old.md": "# History\n"})
    reports, errors = devguide_reports.load_queue("archive/resolved_bugs")
    assert (reports, errors) == ([], [])


def test_readmes_are_not_entries(tmp_path, monkeypatch):
    _queue(tmp_path, monkeypatch, "pending_bugs", {"README.md": "# Index\n"})
    reports, errors = devguide_reports.load_queue("pending_bugs")
    assert (reports, errors) == ([], [])


def test_the_index_groups_by_status_and_links_the_issue():
    body = devguide_index.render(
        [
            _report(name="one.md", status="open"),
            _report(name="two.md", status="active", issue="uibcdf/molsysmt#9"),
        ],
        archived=False,
    )
    assert "### Open (1)" in body
    assert "### In progress (1)" in body
    assert "[`one.md`](one.md)" in body
    assert "https://github.com/uibcdf/molsysmt/issues/9" in body


def test_a_blocked_entry_shows_what_blocks_it():
    body = devguide_index.render(
        [_report(status="blocked", blocked_by=["uibcdf/smonitor#4"])], archived=False
    )
    assert "Blocked by uibcdf/smonitor#4." in body


def test_an_empty_queue_says_so():
    assert devguide_index.render([], archived=False) == "*No entries.*"


def test_a_stale_index_is_reported_and_then_written(tmp_path, monkeypatch):
    entry = "---\n" + "\n".join(
        f"{key}: {'' if value is None else value}"
        for key, value in [
            ("summary", "A defect."),
            ("issue", "uibcdf/molsysmt#137"),
            ("status", "open"),
            ("opened", "2026-08-09"),
            ("severity", "high"),
            ("verification", "reproduced"),
            ("area", "[form]"),
        ]
    ) + "\n---\n\n# Body\n"
    directory = _queue(
        tmp_path,
        monkeypatch,
        "pending_bugs",
        {
            "entry.md": entry,
            "README.md": (
                "# Pending Bugs\n\nHand-written head.\n\n"
                f"{devguide_index.OPEN_MARKER}\n{devguide_index.CLOSE_MARKER}\n"
            ),
        },
    )

    stale, errors = devguide_index.process(check=True)
    assert errors == []
    assert stale == ["devguide/pending_bugs/README.md"]

    devguide_index.process(check=False)
    rendered = (directory / "README.md").read_text(encoding="utf-8")
    assert "Hand-written head." in rendered
    assert "### Open (1)" in rendered
    assert "[`entry.md`](entry.md)" in rendered

    assert devguide_index.process(check=True) == ([], [])


def test_a_readme_without_markers_is_reported(tmp_path, monkeypatch):
    _queue(tmp_path, monkeypatch, "pending_bugs", {"README.md": "# Pending Bugs\n"})
    _, errors = devguide_index.process(check=True)
    assert any("add the generated block markers" in error for error in errors)
