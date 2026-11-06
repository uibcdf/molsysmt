"""Full board acquisition precedes absence checks; rendering can remain bounded."""

import json

import pytest

from devtools.scripts import devguide_issue

API = (
    "api",
    "--paginate",
    "--slurp",
    "repos/{owner}/{repo}/issues?state=all&per_page=100",
)


def test_remote_state_keeps_old_issues_beyond_five_pages_and_filters_prs(monkeypatch):
    # Transport-only records. The two old identities were verified independently
    # on the live owner; 500 recent records keep the original limit observable.
    pages = [
        [
            {
                "number": 1000 + page * 100 + row,
                "title": "transport fixture",
                "state": "open",
                "labels": [],
            }
            for row in range(100)
        ]
        for page in range(5)
    ]
    pages.append(
        [
            {
                "number": 25,
                "title": "Proteins, small molecules and entities names",
                "state": "open",
                "labels": [{"name": "proposal", "color": "ffffff"}],
            },
            {
                "number": 22,
                "title": "Hbonds output formats",
                "state": "closed",
                "labels": [],
            },
            {
                "number": 21,
                "title": "PR transport control",
                "state": "closed",
                "labels": [],
                "pull_request": {"url": "https://example.invalid/pulls/21"},
            },
        ]
    )

    def acquire(*arguments):
        assert arguments == API
        return json.dumps(pages)

    monkeypatch.setattr(devguide_issue, "_gh", acquire)
    actual = devguide_issue._remote_state()
    assert len(actual) == 502
    assert actual[25] == {
        "number": 25,
        "title": "Proteins, small molecules and entities names",
        "state": "OPEN",
        "labels": [{"name": "proposal"}],
    }
    assert actual[22]["state"] == "CLOSED"
    assert 21 not in actual


@pytest.mark.parametrize("pages", [[], [[]]])
def test_remote_state_accepts_a_valid_empty_inventory(monkeypatch, pages):
    monkeypatch.setattr(devguide_issue, "_gh", lambda *args: json.dumps(pages))
    assert devguide_issue._remote_state() == {}


def test_empty_transport_body_is_not_a_confirmed_empty_board(monkeypatch):
    monkeypatch.setattr(devguide_issue, "_gh", lambda *args: "")
    with pytest.raises(json.JSONDecodeError):
        devguide_issue._remote_state()


def test_acquisition_failure_is_not_reported_as_missing_issues(monkeypatch):
    def fail(*arguments):
        raise SystemExit("GitHub acquisition failed")

    monkeypatch.setattr(devguide_issue, "_gh", fail)
    with pytest.raises(SystemExit, match="GitHub acquisition failed"):
        devguide_issue._remote_state()
