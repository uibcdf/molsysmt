"""Keep kernel evidence bounded and independent of browser acceptance."""

import json
from contextlib import contextmanager
from http.client import IncompleteRead
from urllib.error import URLError

import pytest

from tests.molsysviewer_molsysmt import system_panel_jupyter as launcher


def _response(monkeypatch, payload):
    @contextmanager
    def opening(request, *, timeout):
        assert request.get_method() == "GET"
        assert request.full_url == "http://127.0.0.1:12345/api/sessions"
        assert request.get_header("Authorization") == "token PRIVATE_TOKEN"
        assert timeout == 2

        class Response:
            def read(self, size):
                assert size == 65537
                return payload

        yield Response()

    monkeypatch.setattr(launcher, "urlopen", opening)


def test_session_snapshot_keeps_stage_and_discards_credentials_and_source_details(
    monkeypatch,
):
    models = [
        {
            "path": "system.ipynb",
            "id": "PRIVATE_ID",
            "kernel": {
                "id": "PRIVATE_KERNEL",
                "execution_state": "busy",
                "connections": 2,
                "private": "PRIVATE_TOKEN",
            },
        },
        {
            "path": "plain.ipynb",
            "kernel": {"execution_state": "idle", "connections": 1},
        },
        {
            "path": "PRIVATE_SOURCE_PATH",
            "kernel": {"execution_state": "PRIVATE_DETAIL", "connections": True},
        },
    ]
    _response(monkeypatch, json.dumps(models).encode())
    snapshot = launcher._session_snapshot(12345, "PRIVATE_TOKEN")
    assert snapshot == {
        "available": True,
        "session_count": 3,
        "truncated": False,
        "sessions": [
            {"role": "molecular", "execution_state": "busy", "connections": 2},
            {"role": "plain_control", "execution_state": "idle", "connections": 1},
            {"role": "other", "execution_state": "unknown", "connections": None},
        ],
    }
    assert "PRIVATE" not in json.dumps(snapshot)


@pytest.mark.parametrize("payload", [b"not JSON", b"{}", b"x" * 65537])
def test_invalid_or_oversized_diagnostics_remain_unavailable(monkeypatch, payload):
    _response(monkeypatch, payload)
    assert launcher._session_snapshot(12345, "PRIVATE_TOKEN")["available"] is False


def test_empty_sessions_are_distinct_from_unavailable_sessions(monkeypatch):
    _response(monkeypatch, b"[]")
    snapshot = launcher._session_snapshot(12345, "PRIVATE_TOKEN")
    assert snapshot["available"] and snapshot["session_count"] == 0
    assert snapshot["sessions"] == []


def test_session_rows_are_bounded_and_malformed_rows_do_not_become_known_states(
    monkeypatch,
):
    _response(monkeypatch, json.dumps([None] * 50).encode())
    snapshot = launcher._session_snapshot(12345, "PRIVATE_TOKEN")
    assert snapshot["session_count"] == 50 and snapshot["truncated"]
    assert len(snapshot["sessions"]) == 16
    assert {row["execution_state"] for row in snapshot["sessions"]} == {"unknown"}


@pytest.mark.parametrize(
    "failure", [URLError("PRIVATE_TOKEN"), IncompleteRead(b"PRIVATE_TOKEN")]
)
def test_transport_error_is_not_serialized_or_mistaken_for_no_kernel(
    monkeypatch, failure
):
    def unavailable(*args, **kwargs):
        raise failure

    monkeypatch.setattr(launcher, "urlopen", unavailable)
    snapshot = launcher._session_snapshot(12345, "PRIVATE_TOKEN")
    assert snapshot == {"available": False, "reason": type(failure).__name__}
    assert "PRIVATE" not in json.dumps(snapshot)


@pytest.mark.parametrize("completed", [False, True])
def test_record_keeps_browser_verdict_and_no_request_runs_before_server_readiness(
    tmp_path, monkeypatch, completed
):
    def forbidden(*args, **kwargs):
        pytest.fail("An unready or exited server must not receive a diagnostic request")

    monkeypatch.setattr(launcher, "urlopen", forbidden)
    launcher._record_session_snapshot(
        tmp_path, 12345, "PRIVATE_TOKEN", completed=completed, ready=False
    )
    snapshot = json.loads((tmp_path / "kernel-session-state.json").read_text())
    assert snapshot["browser_completed"] is completed
    assert snapshot["available"] is False
    assert "PRIVATE" not in json.dumps(snapshot)


def test_diagnostic_write_failure_does_not_replace_the_attempt_verdict(
    tmp_path, monkeypatch, capsys
):
    _response(monkeypatch, b"[]")
    (tmp_path / "kernel-session-state.json").mkdir()
    launcher._record_session_snapshot(
        tmp_path, 12345, "PRIVATE_TOKEN", completed=False, ready=True
    )
    assert (
        capsys.readouterr().err == "Jupyter session diagnostics could not be stored.\n"
    )
