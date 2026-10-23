"""Native topology export pairs explicit geometry with the same atom subset."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from tests.conversion_truth.test_declared_native_edges import _execute_direct
from tests.native.test_molsys import build_minimal_molsys


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("target", ["file:pdb", "string:pdb_text"])
@pytest.mark.parametrize("selection", ["all", [2, 0]])
@pytest.mark.parametrize("length_unit", ["nm", "angstrom"])
def test_native_topology_pdb_export_preserves_units_selection_and_owner(
    route, target, selection, length_unit, tmp_path
):
    molsys = build_minimal_molsys(n_structures=2)
    coordinates = np.arange(24, dtype=float).reshape(2, 4, 3) / 10
    box = np.repeat(np.diag([4.0, 5.0, 6.0])[None], 2, axis=0)
    factor = 10 if length_unit == "angstrom" else 1
    kwargs = {
        "coordinates": puw.quantity(coordinates * factor, length_unit),
        "box": puw.quantity(box * factor, length_unit),
    }
    if target == "file:pdb":
        kwargs["output_filename"] = str(tmp_path / "export.pdb")
    result = (
        _execute_direct(
            "molsysmt.Topology",
            target,
            molsys.topology,
            atom_indices=selection,
            **kwargs,
        )
        if route == "direct"
        else msm.convert(molsys.topology, to_form=target, selection=selection, **kwargs)
    )
    restored = msm.convert(result, to_form="molsysmt.MolSys", get_missing_bonds=False)
    indices = list(range(4)) if isinstance(selection, str) else [0, 2]
    assert restored.topology.atoms["atom_name"].tolist() == [
        molsys.topology.atoms.at[index, "atom_name"] for index in indices
    ]
    actual = puw.get_value(restored.structures.coordinates, to_unit="nm")
    assert actual.shape == (2, len(indices), 3)
    np.testing.assert_allclose(actual, coordinates[:, indices], atol=5.1e-5, rtol=0)
    np.testing.assert_allclose(
        puw.get_value(restored.structures.box, to_unit="nm"), box, atol=1e-6, rtol=0
    )
    assert molsys.topology._molsys_owner_ref() is molsys
    assert molsys.topology.n_atoms == 4
