"""Runtime settings belong only to the receiving server's bounded lifetime."""

import hashlib
import json
import os
import stat
import sys
from contextlib import nullcontext

import pytest

from tests.molsysviewer_molsysmt import system_panel_jupyter as launcher


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
