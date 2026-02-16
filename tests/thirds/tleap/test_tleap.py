import os
import shutil
from pathlib import Path
import pytest

from molsysmt.thirds.tleap import TLeap


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

    with pytest.raises(RuntimeError, match="Strict mode flagged critical LEaP diagnostics"):
        tleap.run(working_directory=str(workdir), strict=True, verbose=False)


def test_run_reports_missing_tleap_binary(tmp_path):
    tleap = TLeap()
    tleap._tleap_executable = "tleap_binary_that_does_not_exist"
    tleap.save_unit("pep", str(tmp_path / "system.prmtop"))

    with pytest.raises(RuntimeError, match="Could not execute tleap binary"):
        tleap.run(working_directory=str(tmp_path / "workdir"), verbose=False)


def test_sanitize_unit_name_rejects_empty():
    with pytest.raises(ValueError, match="non-empty string"):
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
