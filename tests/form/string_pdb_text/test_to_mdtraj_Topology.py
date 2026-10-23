"""PDB text uses a supported MDTraj file reader and retires its scratch path."""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form.string_pdb_text.to_mdtraj_Topology import to_mdtraj_Topology
from tests.conversion_truth.test_declared_pdb_edges import _pdb_text


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("selection", ["all", [0, 2]])
def test_pdb_text_to_mdtraj_topology_preserves_atom_selection(route, selection):
    pytest.importorskip("mdtraj")
    topology = (
        to_mdtraj_Topology(_pdb_text(), atom_indices=selection)
        if route == "direct"
        else msm.convert(_pdb_text(), to_form="mdtraj.Topology", selection=selection)
    )
    expected = ["O", "H1", "H2"] if isinstance(selection, str) else ["O", "H2"]
    assert [atom.name for atom in topology.atoms] == expected
    assert topology.n_atoms == len(expected)
    assert topology.n_residues == 1
    assert topology.n_bonds == (2 if isinstance(selection, str) else 1)


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("selection", ["all", [0, 2]])
def test_pdb_text_to_mdtraj_trajectory_preserves_selected_structures(route, selection):
    pytest.importorskip("mdtraj")
    from molsysmt.form.string_pdb_text.to_mdtraj_Trajectory import to_mdtraj_Trajectory

    structures = [1, 0, 1]
    trajectory = (
        to_mdtraj_Trajectory(
            _pdb_text(), atom_indices=selection, structure_indices=structures
        )
        if route == "direct"
        else msm.convert(
            _pdb_text(),
            to_form="mdtraj.Trajectory",
            selection=selection,
            structure_indices=structures,
        )
    )
    first = np.array([[0, 0, 0], [0.095, 0, 0], [-0.024, 0.092, 0]])
    coordinates = np.stack([first, first + [0.1, 0.2, 0.3]])
    indices = list(range(3)) if isinstance(selection, str) else selection
    assert trajectory.xyz.shape == (3, len(indices), 3)
    np.testing.assert_allclose(
        trajectory.xyz, coordinates[structures][:, indices], atol=1e-7, rtol=0
    )


@pytest.mark.parametrize("fail", [False, True, "interrupt"])
@pytest.mark.parametrize("target", ["mdtraj.Topology", "mdtraj.Trajectory"])
@pytest.mark.parametrize("route", ["direct", "public"])
def test_pdb_text_retires_owned_scratch_on_success_and_failure(
    monkeypatch, fail, target, route
):
    pytest.importorskip("mdtraj")
    from importlib import import_module

    name = "to_" + target.replace(".", "_")
    module = import_module(f"molsysmt.form.file_pdb.{name}")
    original = getattr(module, name)
    paths = []

    def read(item, **kwargs):
        path = Path(item)
        paths.append(path)
        assert path.is_file()
        assert path.read_text() == _pdb_text()
        if fail:
            if fail == "interrupt":
                raise KeyboardInterrupt("reader interrupted")
            raise RuntimeError("reader failure")
        return original(item, **kwargs)

    monkeypatch.setattr(module, name, read)

    def execute():
        if route == "public":
            return msm.convert(_pdb_text(), to_form=target)
        converter = getattr(
            import_module(f"molsysmt.form.string_pdb_text.{name}"), name
        )
        return converter(_pdb_text())

    if fail:
        error = KeyboardInterrupt if fail == "interrupt" else RuntimeError
        with pytest.raises(error, match="reader"):
            execute()
    else:
        assert execute().n_atoms == 3
    assert len(paths) == 1
    assert not paths[0].exists()
    assert not paths[0].parent.exists()
