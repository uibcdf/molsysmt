import errno
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from molsysmt.third_party.tleap import TLeap


@pytest.mark.parametrize("stage", ["copy", "start", "child", "success"])
def test_owned_workdir_is_retired_on_success_and_failure(monkeypatch, tmp_path, stage):
    """Cover setup failures as well as child outcomes inside the owned scope."""
    workdir = tmp_path / "owned"
    input_file = tmp_path / "input.lib"
    input_file.write_text("caller input")
    sentinel = tmp_path / "caller.log"
    sentinel.write_text("retained evidence")
    original_cwd = Path.cwd()
    tleap = TLeap()
    tleap.load_parameters(str(input_file))
    if stage == "copy":
        input_file.unlink()

    def make_directory():
        workdir.mkdir()
        return str(workdir)

    def run_child(*args, **kwargs):
        assert Path.cwd() == workdir
        if stage == "start":
            raise FileNotFoundError("missing child")
        (workdir / "leap.log").write_text("private child log")
        return subprocess.CompletedProcess(
            args[0], 17 if stage == "child" else 0, stdout=""
        )

    monkeypatch.setattr("tempfile.mkdtemp", make_directory)
    monkeypatch.setattr("subprocess.run", run_child)
    expected_error = {
        "copy": FileNotFoundError,
        "start": RuntimeError,
        "child": RuntimeError,
    }
    if stage == "success":
        assert tleap.run() == []
    else:
        with pytest.raises(expected_error[stage]):
            tleap.run()
    assert not workdir.exists()
    assert Path.cwd() == original_cwd
    assert sentinel.read_text() == "retained evidence"
    if stage != "copy":
        assert input_file.read_text() == "caller input"


def test_owned_workdir_removal_failure_is_visible(monkeypatch, tmp_path):
    """Make an actual rmtree unlink failure visible to the caller."""
    workdir = tmp_path / "owned"
    original_cwd = Path.cwd()
    real_unlink = os.unlink

    def make_directory():
        workdir.mkdir()
        return str(workdir)

    def deny_script_unlink(path, *args, **kwargs):
        if Path(path).name == "leap.in":
            raise PermissionError(errno.EACCES, "scratch retirement denied", str(path))
        return real_unlink(path, *args, **kwargs)

    def run_child(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 0, stdout="")

    monkeypatch.setattr("tempfile.mkdtemp", make_directory)
    monkeypatch.setattr("subprocess.run", run_child)
    monkeypatch.setattr(os, "unlink", deny_script_unlink)
    with pytest.raises(PermissionError, match="scratch retirement denied"):
        TLeap().run()
    assert workdir.exists()
    assert Path.cwd() == original_cwd


def test_save_unit_inpcrd_builds_paired_outputs():
    tleap = TLeap()
    tleap.save_unit("pep", "pep.inpcrd")

    script = tleap.script
    assert "saveAmberParm pep pep.prmtop pep.inpcrd" in script
    assert "pep.inpcrd" in tleap._output_file_paths
    assert "pep.prmtop" in tleap._output_file_paths


def test_run_with_explicit_workdir_copies_inputs_and_outputs(monkeypatch, tmp_path):
    input_file = tmp_path / "input.lib"
    input_file.write_text("dummy", encoding="utf-8")

    output_file = tmp_path / "system.prmtop"
    output_pair = tmp_path / "system.inpcrd"

    tleap = TLeap()
    tleap.load_parameters(str(input_file))
    tleap.save_unit("pep", str(output_file))

    workdir = tmp_path / "workdir"
    workdir.mkdir()
    original_cwd = os.getcwd()

    class DummyProcess:
        returncode = 0
        stdout = "WARNING: test warning from tleap"

    def fake_run(cmd, stdout, stderr, text, check):
        assert cmd == ["tleap", "-f", "leap.in"]
        assert Path.cwd() == workdir
        assert (workdir / "input.lib").exists()
        (workdir / "system.prmtop").write_text("prmtop", encoding="utf-8")
        (workdir / "system.inpcrd").write_text("inpcrd", encoding="utf-8")
        (workdir / "leap.log").write_text("log", encoding="utf-8")
        return DummyProcess()

    monkeypatch.setattr("subprocess.run", fake_run)

    warnings = tleap.run(working_directory=str(workdir), verbose=False)

    assert warnings == ["test warning from tleap"]
    assert output_file.exists()
    assert output_pair.exists()
    assert (tmp_path / "system.leap.log").exists()
    assert os.getcwd() == original_cwd


def test_run_can_return_structured_diagnostics(monkeypatch, tmp_path):
    output_file = tmp_path / "system.prmtop"
    tleap = TLeap()
    tleap.save_unit("pep", str(output_file))

    workdir = tmp_path / "workdir_diag"
    workdir.mkdir()

    class DummyProcess:
        returncode = 0
        stdout = "\n".join(
            [
                "WARNING: one warning",
                "ERROR: one error",
                "FATAL: one fatal issue",
            ]
        )

    def fake_run(cmd, stdout, stderr, text, check):
        (workdir / "system.prmtop").write_text("prmtop", encoding="utf-8")
        (workdir / "system.inpcrd").write_text("inpcrd", encoding="utf-8")
        (workdir / "leap.log").write_text("log", encoding="utf-8")
        return DummyProcess()

    monkeypatch.setattr("subprocess.run", fake_run)
    result = tleap.run(
        working_directory=str(workdir),
        verbose=False,
        return_diagnostics=True,
    )

    assert result["warnings"] == ["one warning"]
    severities = [entry["severity"] for entry in result["diagnostics"]]
    assert severities == ["warning", "error", "fatal"]
    assert result["return_code"] == 0


def test_run_strict_mode_flags_critical_patterns(monkeypatch, tmp_path):
    tleap = TLeap()
    tleap.save_unit("pep", str(tmp_path / "system.prmtop"))

    workdir = tmp_path / "workdir_strict"
    workdir.mkdir()

    class DummyProcess:
        returncode = 0
        stdout = "Could not find bond parameter for: EP - OW"

    def fake_run(cmd, stdout, stderr, text, check):
        (workdir / "system.prmtop").write_text("prmtop", encoding="utf-8")
        (workdir / "system.inpcrd").write_text("inpcrd", encoding="utf-8")
        (workdir / "leap.log").write_text("log", encoding="utf-8")
        return DummyProcess()

    monkeypatch.setattr("subprocess.run", fake_run)

    with pytest.raises(
        RuntimeError, match="Strict mode flagged critical LEaP diagnostics"
    ):
        tleap.run(working_directory=str(workdir), strict=True, verbose=False)


def test_run_reports_missing_tleap_binary(tmp_path):
    tleap = TLeap()
    tleap._tleap_executable = "tleap_binary_that_does_not_exist"
    tleap.save_unit("pep", str(tmp_path / "system.prmtop"))

    with pytest.raises(RuntimeError, match="Could not execute tleap binary"):
        tleap.run(working_directory=str(tmp_path / "workdir"), verbose=False)


def test_sanitize_unit_name_rejects_empty():
    from molsysmt import ArgumentError

    with pytest.raises(ArgumentError):
        TLeap._sanitize_unit_name("")


def test_run_keep_working_directory_when_requested(monkeypatch, tmp_path):
    tleap = TLeap()
    tleap.save_unit("pep", str(tmp_path / "system.prmtop"))

    class DummyProcess:
        returncode = 0
        stdout = "WARNING: test warning from tleap"

    def fake_run(cmd, stdout, stderr, text, check):
        with open("system.prmtop", "w", encoding="utf-8") as file_handle:
            file_handle.write("prmtop")
        with open("system.inpcrd", "w", encoding="utf-8") as file_handle:
            file_handle.write("inpcrd")
        with open("leap.log", "w", encoding="utf-8") as file_handle:
            file_handle.write("log")
        return DummyProcess()

    monkeypatch.setattr("subprocess.run", fake_run)
    result = tleap.run(
        working_directory=None,
        verbose=False,
        keep_working_directory=True,
        return_diagnostics=True,
    )

    assert os.path.isdir(result["working_directory"])
    assert os.path.isfile(os.path.join(result["working_directory"], "leap.in"))
    shutil.rmtree(result["working_directory"], ignore_errors=True)
