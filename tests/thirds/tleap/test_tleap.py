import os
from pathlib import Path

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
