"""Protecting explicit aromatic representation changes and preserved source data."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Structures
from tests.native.test_preparation_history import assert_tree


def declared_source():
    molsys = msm.physchem.get_peptide_chemical_template(
        ["PHE"], "ammonium", "carboxylate"
    )["template"]
    state = molsys.chemical_states._states[0]
    aromatic = state.bonds.index[state.bonds.is_aromatic.eq(True)]
    state.bonds.loc[aromatic, "bond_order"] = [1, 2, 1, 2, 1, 2]
    state.bonds.loc[aromatic, "fractional_bond_order"] = pd.NA
    state.connectivity_completeness = "partial"
    structures = Structures()
    structures.append(
        coordinates=msm.pyunitwizard.quantity(
            np.arange(2 * molsys.get_n_atoms() * 3).reshape(2, -1, 3), "angstrom"
        ),
        box=msm.pyunitwizard.quantity(np.tile(np.eye(3), (2, 1, 1)), "nm"),
        time=msm.pyunitwizard.quantity([0, 1], "fs"),
    )
    molsys.structures = structures
    molsys.interactions = {
        "empty": msm.Interactions.from_records(
            [],
            n_atoms=molsys.get_n_atoms(),
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="control",
        )
    }
    return molsys, np.asarray(aromatic, dtype=np.int64)


def test_normalization_preserves_nonaromatic_chemistry_pose_and_all_other_states(
    tmp_path,
):
    source, aromatic = declared_source()
    source.chemical_states.append_state()
    original = source.copy()
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        result = msm.physchem.normalize_aromatic_bond_orders(source)
    molsys, report = result["molecular_system"], result["report"]
    assert report["status"] == "normalized"
    np.testing.assert_array_equal(report["changed_bond_indices"], aromatic)
    np.testing.assert_array_equal(report["original_bond_orders"], [1, 2, 1, 2, 1, 2])
    assert np.isnan(report["original_fractional_bond_orders"]).all()
    assert report["bonded_atom_pairs"].shape == (6, 2)
    assert report["invalidated_analysis_names"] == ["empty"]
    assert not molsys.interactions["empty"].evaluated_structure_indices.size
    assert source.interactions["empty"].evaluated_structure_indices.tolist() == [0, 1]
    before, after = (
        original.chemical_states._states[0],
        molsys.chemical_states._states[0],
    )
    assert after.connectivity_completeness == "partial"
    assert after.bonds.loc[aromatic, "bond_order"].isna().all()
    assert after.bonds.loc[aromatic, "fractional_bond_order"].eq(1.5).all()
    pd.testing.assert_frame_equal(after.atom_attributes, before.atom_attributes)
    other = after.bonds.index.difference(aromatic)
    pd.testing.assert_frame_equal(after.bonds.loc[other], before.bonds.loc[other])
    pd.testing.assert_frame_equal(
        molsys.chemical_states._states[1].bonds,
        original.chemical_states._states[1].bonds,
    )
    pd.testing.assert_frame_equal(source.chemical_states._states[0].bonds, before.bonds)
    pd.testing.assert_frame_equal(molsys.topology.atoms, original.topology.atoms)
    for field in ("coordinates", "box", "time"):
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(getattr(molsys.structures, field)),
            msm.pyunitwizard.get_value(getattr(original.structures, field)),
        )
        assert msm.pyunitwizard.get_unit(
            getattr(molsys.structures, field)
        ) == msm.pyunitwizard.get_unit(getattr(original.structures, field))
    target = tmp_path / "normalized.h5msm"
    msm.convert(molsys, to_form="file:h5msm", output_filename=str(target))
    loaded = msm.convert(target, to_form="molsysmt.MolSys")
    pd.testing.assert_frame_equal(loaded.chemical_states._states[0].bonds, after.bonds)


@pytest.mark.parametrize(
    "variant",
    ["triple", "fraction", "atom_flag", "stereo", "endpoint", "kind", "duplicate"],
)
def test_incompatible_declared_aromaticity_fails_transactionally(variant):
    molsys, indices = declared_source()
    state = molsys.chemical_states._states[0]
    first, last = int(indices[0]), int(indices[-1])
    if variant == "triple":
        state.bonds.at[last, "bond_order"] = 3
    elif variant == "fraction":
        state.bonds.at[last, "fractional_bond_order"] = 1.7
    elif variant == "atom_flag":
        state.atom_attributes.at[
            int(state.bonds.at[last, "atom1_index"]), "is_aromatic"
        ] = False
    elif variant == "stereo":
        state.bonds.at[last, "stereochemistry"] = "E"
    elif variant == "endpoint":
        state.bonds.at[last, "atom1_index"] = molsys.get_n_atoms()
    elif variant == "kind":
        state.bonds.at[last, "bond_type"] = "dative"
    else:
        state.bonds.loc[last, ["atom1_index", "atom2_index"]] = state.bonds.loc[
            first, ["atom1_index", "atom2_index"]
        ]
    original = deepcopy(state.bonds)
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.normalize_aromatic_bond_orders(molsys)
    pd.testing.assert_frame_equal(state.bonds, original)


def test_unknown_aromaticity_is_not_perceived_and_empty_arrays_are_typed():
    molsys, aromatic = declared_source()
    state = molsys.chemical_states._states[0]
    state.atom_attributes = pd.DataFrame(index=range(molsys.get_n_atoms()))
    state.bonds["is_aromatic"] = pd.NA
    original = state.bonds.copy(deep=True)
    result = msm.physchem.normalize_aromatic_bond_orders(molsys)
    report = result["report"]
    assert report["status"] == "unchanged"
    assert (
        report["bond_indices"].shape == (0,)
        and report["bond_indices"].dtype == np.int64
    )
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert (
        report["original_bond_orders"].shape == (0,)
        and report["original_bond_orders"].dtype == np.float64
    )
    assert report["unassessed_bond_indices"].size == len(original)
    assert result["molecular_system"].interactions[
        "empty"
    ].evaluated_structure_indices.tolist() == [0, 1]
    pd.testing.assert_frame_equal(
        result["molecular_system"].chemical_states._states[0].bonds, original
    )


@pytest.mark.parametrize(
    "form",
    [
        "molsysmt.MolSys",
        "molsysmt.Topology",
        "molsysmt.ChemicalStates",
        "molsysmt.ChemicalStatesDict",
    ],
)
def test_supported_forms_and_nonreference_state(form):
    source, aromatic = declared_source()
    source.interactions = {}
    source.chemical_states._append_state(source.chemical_states._states[0].copy())
    history0 = source.chemical_states.get_preparation_history(0)
    history1 = source.chemical_states.get_preparation_history(1)
    item = (
        source.chemical_states
        if form == "molsysmt.ChemicalStates"
        else msm.convert(source, to_form=form)
    )
    state_index = 1
    result = msm.physchem.normalize_aromatic_bond_orders(
        item, chemical_state=state_index
    )
    states = result["molecular_system"].chemical_states
    assert_tree(states.get_preparation_history(0), history0)
    retained = states.get_preparation_history(1)
    assert_tree(retained[:-1], history1)
    assert retained[-1]["output"]["chemical_state_index"] == 1
    assert_tree(retained[-1]["report"], result["report"])
    assert result["report"]["chemical_state_index"] == state_index
    assert (
        result["molecular_system"]
        .chemical_states._states[state_index]
        .bonds.loc[aromatic, "bond_order"]
        .isna()
        .all()
    )
    if state_index == 1:
        assert (
            result["molecular_system"]
            .chemical_states._states[0]
            .bonds.loc[aromatic, "bond_order"]
            .notna()
            .all()
        )


def test_repeated_normalization_and_coordinate_independent_state_validation():
    source, _ = declared_source()
    first = msm.physchem.normalize_aromatic_bond_orders(source)
    second = msm.physchem.normalize_aromatic_bond_orders(first["molecular_system"])
    assert second["report"]["status"] == "unchanged"
    assert second["report"]["changed_bond_indices"].shape == (0,)
    with pytest.raises(ArgumentError):
        msm.physchem.normalize_aromatic_bond_orders(source, chemical_state="structure")
