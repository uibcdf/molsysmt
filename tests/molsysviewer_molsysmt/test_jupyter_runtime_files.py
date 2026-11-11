"""Runtime settings belong only to the receiving server's bounded lifetime."""

import hashlib
import json
import os
import stat
import sys
from contextlib import nullcontext
from pathlib import Path

import pytest

from tests.molsysviewer_molsysmt import system_panel_jupyter as launcher


@pytest.mark.parametrize("value", ["nan", "inf", "-inf", "0", "-1", "301"])
def test_server_preparation_budget_rejects_unbounded_or_nonpositive_values(value):
    import argparse

    with pytest.raises(argparse.ArgumentTypeError):
        launcher._server_ready_seconds(value)


@pytest.mark.parametrize("value", ["0.1", "20", "90", "300"])
def test_server_preparation_budget_keeps_explicit_finite_seconds(value):
    assert launcher._server_ready_seconds(value) == float(value)


@pytest.mark.parametrize(
    "option,value",
    [
        ("--cycles", "0"),
        ("--cycles", "31"),
        ("--active-seconds", "nan"),
        ("--active-seconds", "inf"),
        ("--active-seconds", "0"),
        ("--active-seconds", "91"),
    ],
)
def test_prolonged_cli_rejects_unbounded_work_before_creating_output(
    tmp_path, monkeypatch, option, value
):
    output = tmp_path / "receiving"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "receiving",
            "--viewer-root",
            str(tmp_path),
            "--output",
            str(output),
            option,
            value,
        ],
    )
    with pytest.raises(SystemExit) as caught:
        launcher.main()
    assert caught.value.code == 2
    assert not output.exists()


def test_fixture_preparation_failure_leaves_no_runtime_credentials(
    tmp_path, monkeypatch
):
    output = tmp_path / "receiving"
    monkeypatch.setattr(
        sys,
        "argv",
        ["receiving", "--viewer-root", str(tmp_path), "--output", str(output)],
    )

    def fail_preparation(*args, **kwargs):
        raise RuntimeError("synthetic fixture preparation failure")

    def forbidden(*args, **kwargs):
        pytest.fail("Fixture preparation failure must occur before server startup")

    monkeypatch.setattr(launcher, "_notebook", fail_preparation)
    monkeypatch.setattr(launcher.subprocess, "Popen", forbidden)
    owned = [output / "settings.json", output / "config/jupyter_server_config.py"]
    try:
        with pytest.raises(RuntimeError, match="synthetic fixture"):
            launcher.main()
        assert not any(path.exists() for path in owned)
    finally:
        # Preserve only hashes of synthetic failed-baseline remnants, never tokens.
        remnants = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in owned
            if path.is_file()
        }
        if remnants:
            (tmp_path / "retired-synthetic-remnants.json").write_text(
                json.dumps(remnants)
            )
        for path in owned:
            path.unlink(missing_ok=True)


@pytest.mark.parametrize("body_failure", [False, True])
def test_runtime_files_have_scoped_private_ownership(tmp_path, body_failure):
    first, second = tmp_path / "settings.json", tmp_path / "config.py"
    expectation = (
        pytest.raises(RuntimeError, match="synthetic body")
        if body_failure
        else nullcontext()
    )
    with expectation:
        with launcher._runtime_files(
            [(first, "synthetic-settings"), (second, "synthetic-config")]
        ):
            assert first.read_text() == "synthetic-settings"
            assert second.read_text() == "synthetic-config"
            if os.name == "posix":
                assert stat.S_IMODE(first.stat().st_mode) == 0o600
                assert stat.S_IMODE(second.stat().st_mode) == 0o600
            if body_failure:
                raise RuntimeError("synthetic body failure")
    assert not first.exists()
    assert not second.exists()


def test_partial_setup_preserves_preexisting_destination_and_retires_owned_file(
    tmp_path,
):
    first, second = tmp_path / "settings.json", tmp_path / "config.py"
    second.write_text("preexisting file")
    before = second.stat()
    with pytest.raises(FileExistsError):
        with launcher._runtime_files(
            [(first, "synthetic-settings"), (second, "new-config")]
        ):
            pytest.fail(
                "A preexisting destination must prevent entering the server scope"
            )
    assert not first.exists()
    assert second.read_text() == "preexisting file"
    assert second.stat().st_ino == before.st_ino


def test_foreign_replacement_is_not_removed_at_scope_exit(tmp_path):
    path, replacement = tmp_path / "settings.json", tmp_path / "replacement"
    replacement.write_text("foreign replacement")
    with launcher._runtime_files([(path, "owned synthetic content")]):
        replacement.replace(path)
    assert path.read_text() == "foreign replacement"


def test_partial_write_failure_closes_and_retires_both_owned_files(
    tmp_path, monkeypatch
):
    import builtins

    first, second = tmp_path / "settings.json", tmp_path / "config.py"
    streams = []

    class FailingWrite:
        def __init__(self, stream):
            self.stream = stream

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return self.stream.__exit__(*args)

        def fileno(self):
            return self.stream.fileno()

        def write(self, text):
            self.stream.write("partial synthetic content")
            raise OSError("synthetic write failure")

    def opening(path, *args, **kwargs):
        stream = builtins.open(path, *args, **kwargs)
        streams.append(stream)
        return FailingWrite(stream) if path == second else stream

    monkeypatch.setattr(launcher, "open", opening, raising=False)
    with pytest.raises(OSError, match="synthetic write"):
        with launcher._runtime_files([(first, "settings"), (second, "config")]):
            pytest.fail("A partial setup failure must not start the server")
    assert all(stream.closed for stream in streams)
    assert not first.exists()
    assert not second.exists()


@pytest.mark.parametrize("body_failure", [False, True])
def test_cleanup_failure_is_reported_without_skipping_other_owned_files(
    tmp_path, monkeypatch, body_failure
):
    first, second = tmp_path / "settings.json", tmp_path / "config.py"
    original_unlink = type(first).unlink

    def unlink(path, *args, **kwargs):
        if path == second:
            raise PermissionError("synthetic cleanup failure")
        return original_unlink(path, *args, **kwargs)

    monkeypatch.setattr(type(first), "unlink", unlink)
    try:
        with pytest.raises(BaseExceptionGroup) as caught:
            with launcher._runtime_files(
                [(first, "synthetic-settings"), (second, "synthetic-config")]
            ):
                if body_failure:
                    raise RuntimeError("synthetic body failure")
        assert not first.exists()
        assert second.exists()
        assert any(
            isinstance(error, PermissionError) for error in caught.value.exceptions
        )
        assert (
            any(isinstance(error, RuntimeError) for error in caught.value.exceptions)
            == body_failure
        )
    finally:
        original_unlink(second, missing_ok=True)


def test_actual_launcher_preserves_foreign_replacements_after_startup_failure(
    tmp_path, monkeypatch
):
    output = tmp_path / "receiving"
    monkeypatch.setattr(
        sys,
        "argv",
        ["receiving", "--viewer-root", str(tmp_path), "--output", str(output)],
    )
    paths = [output / "settings.json", output / "config/jupyter_server_config.py"]

    def fail_startup(*args, **kwargs):
        for path in paths:
            assert path.is_file()
            replacement = path.with_name(path.name + ".foreign")
            replacement.write_text("foreign replacement")
            replacement.replace(path)
        raise RuntimeError("synthetic startup failure after replacement")

    def node_version(command, **kwargs):
        assert command == ["/usr/bin/node", "--version"]
        return "synthetic-node-version"

    monkeypatch.setattr(launcher.subprocess, "check_output", node_version)
    monkeypatch.setattr(launcher.subprocess, "Popen", fail_startup)
    with pytest.raises(RuntimeError, match="synthetic startup failure"):
        launcher.main()
    assert all(path.read_text() == "foreign replacement" for path in paths)


@pytest.mark.parametrize(
    "response, budget, ready, probes",
    [
        ("success", None, True, 1),
        ("success", "0.1", True, 1),
        ("late", "0.1", False, 1),
        ("at-deadline", "0.1", False, 1),
        ("timeout", "0.1", False, 1),
        ("exit", "0.1", False, 0),
    ],
)
def test_launcher_readiness_obeys_deadline_and_retires_owned_files(
    tmp_path, monkeypatch, response, budget, ready, probes
):
    from contextlib import contextmanager
    from types import SimpleNamespace
    from urllib.error import URLError

    output = tmp_path / "receiving"
    argv = ["receiving", "--viewer-root", str(tmp_path), "--output", str(output)]
    if budget is not None:
        argv.extend(["--server-ready-timeout", budget])
    monkeypatch.setattr(sys, "argv", argv)
    now = 0.0
    sleeps = []
    requests = []
    browser_calls = []

    def sleep(seconds):
        nonlocal now
        sleeps.append(seconds)
        now += seconds

    class Server:
        pid = 42
        returncode = 7 if response == "exit" else None

        def poll(self):
            return self.returncode

        def wait(self, timeout):
            self.returncode = 0
            return self.returncode

    server = Server()

    @contextmanager
    def urlopen(request, timeout):
        nonlocal now
        assert request.get_header("Authorization").startswith("token ")
        if request.full_url.endswith("/api/sessions"):
            yield SimpleNamespace(read=lambda _: b"[]")
            return
        if request.full_url.endswith("/api/shutdown"):
            assert request.get_method() == "POST"
            yield SimpleNamespace(status=200)
            return
        assert request.full_url.endswith("/api/status")
        requests.append(timeout)
        if response == "timeout":
            now += 0.02
            raise URLError("synthetic request timeout")
        now += {"success": 0.05, "late": 0.2, "at-deadline": 0.1}[response]
        yield SimpleNamespace(status=200)

    monkeypatch.setattr(
        launcher, "time", SimpleNamespace(monotonic=lambda: now, sleep=sleep)
    )
    monkeypatch.setattr(launcher, "urlopen", urlopen)
    monkeypatch.setattr(launcher.subprocess, "Popen", lambda *args, **kwargs: server)
    monkeypatch.setattr(
        launcher.subprocess, "check_output", lambda *args, **kwargs: "node"
    )
    monkeypatch.setattr(
        launcher.subprocess,
        "run",
        lambda command, **kwargs: browser_calls.append(command),
    )

    expectation = (
        nullcontext()
        if ready
        else pytest.raises(RuntimeError, match="Isolated Jupyter")
    )
    with expectation:
        launcher.main()

    startup = json.loads((output / "server-startup.json").read_text())
    limit = float(budget) if budget is not None else 20.0
    assert startup["budget_seconds"] == limit
    assert startup["ready"] is ready
    assert len(requests) == probes
    if probes:
        assert requests[0] == pytest.approx(min(1.0, limit))
    assert bool(browser_calls) is ready
    if response == "exit":
        assert startup["native_exit_observed"] == 7
    if response == "timeout":
        assert sleeps == pytest.approx([0.08])
    assert startup["elapsed_seconds"] == pytest.approx(now)
    assert server.poll() is not None
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


@pytest.mark.parametrize("active_seconds", ["80", "90"])
def test_prolonged_cli_rejects_playback_exhausting_browser_deadline(
    tmp_path, monkeypatch, active_seconds
):
    output = tmp_path / "receiving"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "receiving",
            "--viewer-root",
            str(tmp_path),
            "--output",
            str(output),
            "--scenario",
            "prolonged-session",
            "--cycles",
            "30",
            "--active-seconds",
            active_seconds,
        ],
    )
    monkeypatch.syspath_prepend(str(Path(launcher.__file__).parent))

    def forbidden(*args, **kwargs):
        pytest.fail("An impossible profile must be rejected before server startup")

    monkeypatch.setattr(launcher.subprocess, "Popen", forbidden)
    monkeypatch.setattr(
        launcher.subprocess, "check_output", lambda *args, **kwargs: "node"
    )
    with pytest.raises(SystemExit) as caught:
        launcher.main()
    assert caught.value.code == 2
    assert not output.exists()
