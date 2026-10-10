"""Verifying intermediate-file custody at the Simulation/PDBFixer bridge."""

from importlib import import_module
from pathlib import Path

import pytest


@pytest.mark.parametrize("stage", ["write", "read", "success"])
def test_pdbfixer_bridge_retires_intermediates(monkeypatch, tmp_path, stage):
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.setattr("tempfile.tempdir", str(scratch))
    caller_file = tmp_path / "caller.pdb"
    caller_file.write_text("caller result\n")
    observed = {}
    error = RuntimeError(f"{stage} failed")
    result = object()

    def write(item, output_filename, **kwargs):
        path = Path(output_filename)
        observed["file"] = path
        path.write_text("partial intermediate\n")
        if stage == "write":
            raise error
        return str(path)

    def read(filename, **kwargs):
        assert Path(filename) == observed["file"]
        assert Path(filename).read_text() == "partial intermediate\n"
        if stage == "read":
            raise error
        return result

    writer = import_module("molsysmt.form.openmm_Simulation.to_file_pdb")
    reader = import_module("molsysmt.form.file_pdb.to_pdbfixer_PDBFixer")
    bridge = import_module("molsysmt.form.openmm_Simulation.to_pdbfixer_PDBFixer")
    monkeypatch.setattr(writer, "to_file_pdb", write)
    monkeypatch.setattr(reader, "to_pdbfixer_PDBFixer", read)
    if stage == "success":
        assert bridge.to_pdbfixer_PDBFixer(object(), skip_digestion=True) is result
    else:
        with pytest.raises(RuntimeError) as caught:
            bridge.to_pdbfixer_PDBFixer(object(), skip_digestion=True)
        assert caught.value is error
    assert not observed["file"].exists()
    assert list(scratch.iterdir()) == []
    assert caller_file.read_text() == "caller result\n"


def test_pdbfixer_bridge_exposes_retirement_errors(monkeypatch, tmp_path):
    import shutil

    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.setattr("tempfile.tempdir", str(scratch))
    writer = import_module("molsysmt.form.openmm_Simulation.to_file_pdb")
    reader = import_module("molsysmt.form.file_pdb.to_pdbfixer_PDBFixer")
    bridge = import_module("molsysmt.form.openmm_Simulation.to_pdbfixer_PDBFixer")

    def write(item, output_filename, **kwargs):
        Path(output_filename).write_text("intermediate\n")
        return output_filename

    def reject_retirement(*args, **kwargs):
        raise OSError("retirement denied")

    monkeypatch.setattr(writer, "to_file_pdb", write)
    monkeypatch.setattr(
        reader, "to_pdbfixer_PDBFixer", lambda *args, **kwargs: object()
    )
    with monkeypatch.context() as disposal:
        disposal.setattr(shutil, "rmtree", reject_retirement)
        with pytest.raises(OSError, match="retirement denied"):
            bridge.to_pdbfixer_PDBFixer(object(), skip_digestion=True)
    for directory in scratch.iterdir():
        shutil.rmtree(directory)


def test_real_fixer_remains_usable_after_scratch_retirement(monkeypatch, tmp_path):
    import numpy as np

    openmm = pytest.importorskip("openmm")
    pytest.importorskip("pdbfixer")
    from openmm import app, unit

    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.setattr("tempfile.tempdir", str(scratch))
    topology = app.Topology()
    group = topology.addResidue("UNK", topology.addChain())
    topology.addAtom("C", app.element.carbon, group)
    system = openmm.System()
    system.addParticle(12 * unit.dalton)
    simulation = app.Simulation(
        topology,
        system,
        openmm.VerletIntegrator(0.001 * unit.picosecond),
        openmm.Platform.getPlatformByName("Reference"),
    )
    simulation.context.setPositions([[0.1, 0.2, 0.3]] * unit.nanometer)

    bridge = import_module("molsysmt.form.openmm_Simulation.to_pdbfixer_PDBFixer")
    fixer = bridge.to_pdbfixer_PDBFixer(simulation)

    assert list(scratch.iterdir()) == []
    assert fixer.topology.getNumAtoms() == 1
    np.testing.assert_allclose(
        fixer.positions.value_in_unit(unit.nanometer),
        [[0.1, 0.2, 0.3]],
    )
