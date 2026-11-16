"""Receive the chosen Node executable without starting Jupyter or a browser."""

import json
import os
import sys
from pathlib import Path

import pytest

from tests.molsysviewer_molsysmt import system_panel_jupyter as launcher


class BeforeServer(RuntimeError):
    """Stop the real launcher at the owned server boundary."""


def _executable(directory, name="node"):
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (name + ".exe" if os.name == "nt" else name)
    path.write_bytes(b"synthetic executable; never executed by this unit fixture")
    path.chmod(0o700)
    return path.resolve()


def _prepare(monkeypatch, tmp_path, arguments=()):
    output = tmp_path / "receiving"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "receiver",
            "--viewer-root",
            str(tmp_path),
            "--output",
            str(output),
            *arguments,
        ],
    )
    monkeypatch.delenv("MOLSYSVIEWER_NODE", raising=False)
    monkeypatch.setattr(launcher.importlib.metadata, "version", lambda _: "synthetic")

    def before_server(*args, **kwargs):
        raise BeforeServer("reached server boundary")

    monkeypatch.setattr(launcher.subprocess, "Popen", before_server)
    return output


def test_path_node_is_used_and_recorded_without_a_global_node(tmp_path, monkeypatch):
    output = _prepare(monkeypatch, tmp_path)
    selected = _executable(tmp_path / "custom environment" / "bin")
    monkeypatch.setenv("PATH", str(selected.parent))
    if os.name == "nt":
        monkeypatch.setenv("PATHEXT", ".EXE")
    calls = []

    def version(command, **kwargs):
        calls.append(command)
        if command != [str(selected), "--version"]:
            raise FileNotFoundError("No global Node is supplied by this fixture")
        return "v22.14.0\n"

    monkeypatch.setattr(launcher.subprocess, "check_output", version)
    with pytest.raises(BeforeServer, match="server boundary"):
        launcher.main()
    observed = json.loads((output / "environment.json").read_text())
    assert observed["node"] == "v22.14.0"
    assert observed["node_runtime"]["executable"] == str(selected)
    assert observed["node_runtime"]["selection"] == "PATH"
    assert calls == [[str(selected), "--version"]]
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


@pytest.mark.parametrize(
    "choice", ["environment", "cli-path", "cli-name", "cli-over-env"]
)
def test_explicit_node_selection_is_preserved_in_the_actual_launcher(
    tmp_path, monkeypatch, choice
):
    selected = _executable(tmp_path / "chosen prefix" / "bin", "selected-node")
    path_node = _executable(tmp_path / "other prefix" / "bin")
    arguments = ["--node", selected.name if choice == "cli-name" else str(selected)]
    output = _prepare(
        monkeypatch, tmp_path, [] if choice == "environment" else arguments
    )
    monkeypatch.setenv(
        "PATH", os.pathsep.join([str(path_node.parent), str(selected.parent)])
    )
    if os.name == "nt":
        monkeypatch.setenv("PATHEXT", ".EXE")
    if choice in {"environment", "cli-over-env"}:
        monkeypatch.setenv(
            "MOLSYSVIEWER_NODE", str(selected if choice == "environment" else path_node)
        )
    calls = []

    def version(command, **kwargs):
        assert command == [str(selected), "--version"]
        assert kwargs["timeout"] == 10
        calls.append(command)
        return "v22.14.0\n"

    monkeypatch.setattr(launcher.subprocess, "check_output", version)
    with pytest.raises(BeforeServer):
        launcher.main()
    record = json.loads((output / "environment.json").read_text())
    assert record["node_runtime"]["executable"] == str(selected)
    assert record["node_runtime"]["selection"] == (
        "environment" if choice == "environment" else "CLI"
    )
    assert record["node_runtime"]["version"] == record["node"] == "v22.14.0"
    assert len(calls) == 1


@pytest.mark.parametrize(
    "choice",
    [
        "missing-path",
        "missing-cli",
        "nonexecutable",
        "directory",
        "empty-env",
        "missing-env",
    ],
)
def test_invalid_node_does_not_fallback_or_create_runtime_files(
    tmp_path, monkeypatch, capsys, choice
):
    valid = _executable(tmp_path / "valid" / "bin")
    invalid = tmp_path / "invalid-node"
    if choice == "nonexecutable":
        invalid.write_text("not executable")
        invalid.chmod(0o600)
        if os.name == "nt":
            invalid = invalid.with_suffix(".missing")
    elif choice == "directory":
        invalid.mkdir()
    args = (
        ["--node", str(invalid)]
        if choice in {"missing-cli", "nonexecutable", "directory"}
        else []
    )
    output = _prepare(monkeypatch, tmp_path, args)
    monkeypatch.setenv(
        "PATH",
        str(tmp_path / "empty") if choice == "missing-path" else str(valid.parent),
    )
    if choice in {"empty-env", "missing-env"}:
        monkeypatch.setenv(
            "MOLSYSVIEWER_NODE", "" if choice == "empty-env" else str(invalid)
        )

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid executable selection must fail before a child starts")

    monkeypatch.setattr(launcher.subprocess, "check_output", forbidden)
    with pytest.raises(SystemExit) as caught:
        launcher.main()
    assert caught.value.code == 2
    assert "Node executable" in capsys.readouterr().err
    assert not output.exists()


@pytest.mark.parametrize(
    "failure", ["oserror", "nonzero", "timeout", "not-node", "empty"]
)
def test_failed_or_wrong_version_probe_does_not_start_a_server(
    tmp_path, monkeypatch, capsys, failure
):
    selected = _executable(tmp_path / "selected" / "bin")
    output = _prepare(monkeypatch, tmp_path, ["--node", str(selected)])
    calls = []

    def version(command, **kwargs):
        assert command == [str(selected), "--version"]
        assert kwargs["timeout"] == 10
        calls.append(command)
        if failure == "oserror":
            raise PermissionError("synthetic execution denial")
        if failure == "nonzero":
            raise launcher.subprocess.CalledProcessError(3, command)
        if failure == "timeout":
            raise launcher.subprocess.TimeoutExpired(command, 10)
        return "Python 3.14.7" if failure == "not-node" else ""

    monkeypatch.setattr(launcher.subprocess, "check_output", version)
    monkeypatch.setattr(
        launcher.subprocess,
        "Popen",
        lambda *args, **kwargs: pytest.fail("Bad Node must not start Jupyter"),
    )
    with pytest.raises(SystemExit) as caught:
        launcher.main()
    assert caught.value.code == 2
    assert "Node" in capsys.readouterr().err
    assert len(calls) == 1
    assert not (output / "environment.json").exists()
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_real_non_node_binary_is_not_accepted_as_node():
    with pytest.raises(ValueError, match="did not report a Node version"):
        launcher._node_version(sys.executable)


def test_prolonged_pytest_wrapper_inherits_the_selected_node(tmp_path, monkeypatch):
    from tests.molsysviewer_molsysmt import jupyter_receiving_guard as guard

    output = _prepare(monkeypatch, tmp_path)
    selected = _executable(tmp_path / "guard environment" / "bin")
    monkeypatch.setenv("MOLSYSVIEWER_ROOT", str(tmp_path / "viewer"))
    monkeypatch.setenv("MOLSYSVIEWER_NODE", str(selected))
    monkeypatch.syspath_prepend(str(Path(launcher.__file__).parent))
    monkeypatch.setattr(
        launcher.subprocess,
        "check_output",
        lambda command, **kwargs: (
            "v22.14.0"
            if command == [str(selected), "--version"]
            else pytest.fail("The wrapper's selected Node was lost")
        ),
    )
    commands = []

    def selected_receiver(command, **kwargs):
        assert command[0] == sys.executable
        assert Path(command[1]).name == "system_panel_jupyter.py"
        assert kwargs["timeout"] == 360
        assert kwargs.get("env", os.environ)["MOLSYSVIEWER_NODE"] == str(selected)
        commands.append(command)
        monkeypatch.setattr(sys, "argv", command[1:])
        launcher.main()

    monkeypatch.setattr(guard.subprocess, "run", selected_receiver)
    with pytest.raises(BeforeServer):
        guard.test_actual_jupyter_prolonged_popup_controls(tmp_path)
    assert len(commands) == 1
    actual = tmp_path / "jupyter-prolonged-controls" / "environment.json"
    assert json.loads(actual.read_text())["node_runtime"]["executable"] == str(selected)
    assert not output.exists()
