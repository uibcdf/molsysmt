"""Modeller PDB exports retain matched atom names and Cartesian positions."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("selection", ["all", [2, 0]])
def test_modeller_pdb_export_preserves_selected_positions(
    builder_openmm_topology, route, selection, tmp_path
):
    pytest.importorskip("openmm")
    from openmm import app, unit

    from molsysmt.form.openmm_Modeller.to_file_pdb import to_file_pdb

    coordinates = np.arange(12, dtype=float).reshape(4, 3) / 10
    source = app.Modeller(builder_openmm_topology, coordinates * 10 * unit.angstrom)
    filename = str(tmp_path / "export.pdb")
    result = (
        to_file_pdb(
            source,
            atom_indices=selection,
            structure_indices=[0],
            output_filename=filename,
        )
        if route == "direct"
        else msm.convert(
            source,
            to_form="file:pdb",
            selection=selection,
            structure_indices=[0],
            output_filename=filename,
        )
    )
    restored = msm.convert(result, to_form="molsysmt.MolSys", get_missing_bonds=False)
    indices = list(range(4)) if isinstance(selection, str) else [0, 2]
    assert restored.topology.atoms["atom_name"].tolist() == [
        atom.name for atom in source.topology.atoms() if atom.index in indices
    ]
    actual = puw.get_value(restored.structures.coordinates, to_unit="nm")
    assert actual.shape == (1, len(indices), 3)
    np.testing.assert_allclose(actual[0], coordinates[indices], atol=5.1e-5, rtol=0)
    assert source.topology.getNumAtoms() == 4
