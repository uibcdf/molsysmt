"""Protecting molecular mechanics values when mixed queries use reduced pipes."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolecularMechanics, MolSys, Structures, Topology


@pytest.mark.parametrize("selection", ["all", [2, 0]])
def test_mixed_pipes_preserve_mechanics_and_requested_keys(monkeypatch, selection):
    from molsysmt.form import molsysmt_MolSys as adapter

    monkeypatch.setattr(adapter, "piped_topological_attribute", "molsysmt.Topology")
    monkeypatch.setattr(adapter, "piped_structural_attribute", "molsysmt.Structures")
    monkeypatch.setattr(adapter, "piped_any_attribute", None)
    molsys = MolSys()
    molsys.topology = Topology(n_atoms=3)
    molsys.topology.atoms["atom_type"] = ["C", "N", "O"]
    molsys.structures = Structures()
    coordinates = np.arange(9, dtype=float).reshape(1, 3, 3)
    molsys.structures.append(coordinates=msm.pyunitwizard.quantity(coordinates, "nm"))
    molsys.molecular_mechanics = MolecularMechanics(
        atom_ff_type=["CT", "N", "O"], partial_charge=[0.2, -0.3, 0.1]
    )
    output = msm.get(
        molsys,
        element="atom",
        selection=selection,
        output_type="dictionary",
        atom_type=True,
        atom_ff_type=True,
        partial_charge=True,
        coordinates=True,
    )
    indices = [0, 1, 2] if selection == "all" else [2, 0]
    assert set(output) == {"atom_type", "atom_ff_type", "partial_charge", "coordinates"}
    np.testing.assert_array_equal(
        output["atom_type"], np.asarray(["C", "N", "O"])[indices]
    )
    np.testing.assert_array_equal(
        output["atom_ff_type"], np.asarray(["CT", "N", "O"])[indices]
    )
    np.testing.assert_allclose(
        output["partial_charge"].astype(float), np.array([0.2, -0.3, 0.1])[indices]
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(output["coordinates"], to_unit="nm"),
        coordinates[:, indices],
    )
    np.testing.assert_array_equal(
        molsys.molecular_mechanics.atom_ff_type, ["CT", "N", "O"]
    )
