"""An area tag with no label on the board must not cost more than itself.

Guard for `uibcdf/molsysmt#159`. `gh` validates every label in a call against the
repository and rejects the whole command if one is unknown, so a single unknown area
tag stopped every other label from being applied — the state label included. That is
the part that matters: `blocked`, `partial` and `in-progress` are derived from
`status`, so while a label was missing the board kept saying a theme was open and
unstarted when its document said it was blocked.

The two commands need different answers. `open` must refuse before it creates
anything, because a failure there leaves neither the issue nor its document and the
protocol's first step — open the issue to obtain the number — cannot complete. `sync`
must apply what it can and name what it cannot, because refusing outright is what
left the board stale.

`gh` is not called here: `_board_labels` and `_gh` are replaced, so the test runs
offline and asserts the decision rather than the network.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPOSITORY_ROOT / 'devtools' / 'scripts' / 'devguide_issue.py'


@pytest.fixture(scope='module')
def devguide_issue():
    specification = importlib.util.spec_from_file_location('devguide_issue_under_test', SCRIPT)
    module = importlib.util.module_from_spec(specification)
    sys.modules['devguide_issue_under_test'] = module
    specification.loader.exec_module(module)
    return module


BOARD = {'bug', 'proposal', 'docs', 'build', 'api', 'tests', 'blocked', 'partial', 'in-progress'}


def test_missing_labels_reports_only_what_the_board_lacks(devguide_issue, monkeypatch):
    monkeypatch.setattr(devguide_issue, '_board_labels', lambda: set(BOARD))

    assert devguide_issue._missing_labels(['bug', 'docs']) == []
    assert devguide_issue._missing_labels(['bug', 'diagnostics']) == ['diagnostics']
    assert devguide_issue._missing_labels(['zzz', 'aaa']) == ['aaa', 'zzz']


def test_open_refuses_before_creating_anything(devguide_issue, monkeypatch, tmp_path):
    """The issue and the document are both lost on a failure, so nothing may start."""
    called = []
    monkeypatch.setattr(devguide_issue, '_board_labels', lambda: set(BOARD))
    monkeypatch.setattr(devguide_issue, '_gh', lambda *arguments, **keywords: called.append(arguments))

    arguments = type(
        'Arguments', (),
        {'kind': 'bug', 'title': 'A probe', 'area': 'docs,diagnostics',
         'severity': 'medium', 'queue': None, 'today': None},
    )()

    with pytest.raises(SystemExit) as failure:
        devguide_issue.command_open(arguments)

    message = str(failure.value)
    assert 'diagnostics' in message
    assert 'Nothing was created' in message
    assert 'gh label create' in message
    assert 'docs' in message, 'the message should list the labels that do exist'
    assert not called, f'`gh` was called before validating: {called}'


def test_open_proceeds_when_every_label_exists(devguide_issue, monkeypatch):
    """The refusal must be about the missing label, not about validating at all."""
    monkeypatch.setattr(devguide_issue, '_board_labels', lambda: set(BOARD))
    monkeypatch.setattr(devguide_issue, '_missing_labels', lambda labels: [])

    reached = []

    def fake_gh(*arguments, **keywords):
        reached.append(arguments)
        raise SystemExit('stopped after the label check')

    monkeypatch.setattr(devguide_issue, '_gh', fake_gh)

    arguments = type(
        'Arguments', (),
        {'kind': 'bug', 'title': 'A probe', 'area': 'docs,build',
         'severity': 'medium', 'queue': None, 'today': None},
    )()

    with pytest.raises(SystemExit) as failure:
        devguide_issue.command_open(arguments)

    assert 'stopped after the label check' in str(failure.value)
    assert reached, 'validation blocked a call whose labels all exist'


def test_sync_leaves_closed_issues_alone(devguide_issue, monkeypatch, capsys):
    """A closed issue is history, and chasing it keeps `sync --check` from ever passing.

    Before this, an archived report whose issue carried different labels counted as
    drift for ever, so the check could not return 0 and stopped being read. The
    command exists to keep the open board agreeing with the open queues.
    """
    seen = []

    def fake_drift(report, issue):
        seen.append(report)
        return ['drift']

    monkeypatch.setattr(devguide_issue, '_drift', fake_drift)
    monkeypatch.setattr(devguide_issue, '_board_labels', lambda: set(BOARD))
    monkeypatch.setattr(
        devguide_issue, '_remote_state',
        lambda: {1: {'number': 1, 'state': 'CLOSED', 'labels': [], 'title': 'archived'},
                 2: {'number': 2, 'state': 'OPEN', 'labels': [], 'title': 'live'}},
    )

    class FakeReport:
        def __init__(self, number):
            self.issue_number = number
            self.relative = f'report-{number}.md'
            self.labels = ['bug']

    monkeypatch.setattr(
        devguide_issue, 'load_all',
        lambda include_archives=True: ([FakeReport(1), FakeReport(2)], []),
    )

    arguments = type('Arguments', (), {'check': True})()
    devguide_issue.command_sync(arguments)

    checked = {report.issue_number for report in seen}
    assert 1 not in checked, 'the closed issue was still checked for drift'
    assert 2 in checked, 'the open issue must still be checked'
