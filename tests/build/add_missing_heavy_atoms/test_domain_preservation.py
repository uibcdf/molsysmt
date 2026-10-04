"""Protecting declared native domains when heavy-atom repair expands the atom axis."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    StructuralAttributeDropWarning,
    StructuralInconsistencyError,
)


def incomplete_serine(missing_og=True):
    molsys = msm.build.build_peptide("SerAla", engine="MolSysMT")
    selection = 'atom_type != "H"'
    if missing_og:
        selection += ' and atom_name != "OG"'
    molsys = msm.extract(molsys, selection=selection)
    state = molsys.chemical_states._states[0]
    state.state_id = "declared-before-repair"
    state.provenance_index = 2
    state.connectivity_completeness = "partial"
    state.set_atom_attribute("formal_charge", [0] * molsys.get_n_atoms())
    state.set_atom_attribute("is_aromatic", [False] * molsys.get_n_atoms())
    molsys.interactions = {
        "declared-analysis": msm.Interactions.from_records(
            [
                {
                    "structure_index": 0,
                    "interaction_type": "control_pair",
                    "participants": [
                        {"role": "first", "atom_indices": [0]},
                        {"role": "second", "atom_indices": [molsys.get_n_atoms() - 1]},
                    ],
                }
            ],
            n_atoms=molsys.get_n_atoms(),
            n_structures=1,
            evaluated_structure_indices=[0],
            method="independent-control",
        )
    }
    molsys._structure_chemical_state_indices = np.array([0], dtype=np.int64)
    return molsys


@pytest.mark.parametrize("operation", ["heavy", "caps"])
def test_repair_retains_atom_chemistry_state_metadata_and_named_analysis(
    tmp_path, operation
):
    source = incomplete_serine(missing_og=operation == "heavy")
    original = source.copy()
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        with pytest.warns(StructuralAttributeDropWarning, match="atoms_ff"):
            if operation == "heavy":
                output = msm.build.add_missing_heavy_atoms(source)
            else:
                output = msm.build.add_missing_terminal_cappings(
                    source, N_terminal="ACE", C_terminal="NME", engine="MolSysMT"
                )
    source_ids = original.topology.atoms.atom_id.tolist()
    old_to_new = np.asarray(
        [
            output.topology.atoms.index[output.topology.atoms.atom_id.eq(identifier)][0]
            for identifier in source_ids
        ],
        dtype=np.int64,
    )
    old, new = original.chemical_states._states[0], output.chemical_states._states[0]
    assert output.get_n_atoms() == source.get_n_atoms() + (
        1 if operation == "heavy" else 12
    )
    assert output.topology.atoms.atom_id.is_unique
    assert new.state_id == old.state_id and new.provenance_index == old.provenance_index
    pd.testing.assert_frame_equal(
        new.atom_attributes.iloc[old_to_new].reset_index(drop=True), old.atom_attributes
    )
    added = output.topology.atoms.index[~output.topology.atoms.atom_id.isin(source_ids)]
    assert new.atom_attributes.loc[added].isna().all().all()
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm")[
            :, old_to_new
        ],
        msm.pyunitwizard.get_value(original.structures.coordinates, to_unit="nm"),
    )
    np.testing.assert_array_equal(output._structure_chemical_state_indices, [0])
    analysis = output.interactions["declared-analysis"]
    assert analysis.method == "independent-control"
    assert analysis.n_atoms == output.get_n_atoms()
    assert analysis.evaluated_structure_indices.size == 0
    np.testing.assert_array_equal(
        analysis.atom_source_indices[old_to_new], np.arange(len(source_ids))
    )
    np.testing.assert_array_equal(analysis.atom_source_indices[added], -1)
    np.testing.assert_array_equal(analysis.participant_atoms, old_to_new[[0, -1]])
    assert source.interactions[
        "declared-analysis"
    ].evaluated_structure_indices.tolist() == [0]
    pd.testing.assert_frame_equal(source.topology.atoms, original.topology.atoms)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes, old.atom_attributes
    )
    path = tmp_path / "repaired.h5msm"
    msm.convert(output, to_form="file:h5msm", output_filename=str(path))
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert loaded.chemical_states._states[0].state_id == old.state_id
    pd.testing.assert_frame_equal(
        loaded.chemical_states._states[0].atom_attributes, new.atom_attributes
    )
    assert (
        loaded.interactions["declared-analysis"].evaluated_structure_indices.size == 0
    )


def test_multiple_chemical_states_fail_before_atom_domain_expansion():
    source = incomplete_serine()
    source.chemical_states._append_state(source.chemical_states._states[0].copy())
    original = source.copy()
    with pytest.raises(StructuralInconsistencyError, match="one chemical state"):
        msm.build.add_missing_heavy_atoms(source)
    pd.testing.assert_frame_equal(source.topology.atoms, original.topology.atoms)
    assert source.chemical_states.n_chemical_states == 2
    assert source.interactions[
        "declared-analysis"
    ].evaluated_structure_indices.tolist() == [0]


@pytest.mark.parametrize("attribute", ["atoms_ff", "b_factor"])
def test_strict_attribute_policy_rejects_expansion_transactionally(attribute):
    source = incomplete_serine()
    if attribute == "b_factor":
        source.molecular_mechanics.atoms_ff = None
        source.structures.b_factor = np.ones((1, source.get_n_atoms()))
    original = source.copy()
    with pytest.raises(StructuralInconsistencyError, match=attribute):
        msm.build.add_missing_heavy_atoms(source, attribute_policy="strict")
    pd.testing.assert_frame_equal(source.topology.atoms, original.topology.atoms)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes,
        original.chemical_states._states[0].atom_attributes,
    )
    assert source.interactions[
        "declared-analysis"
    ].evaluated_structure_indices.tolist() == [0]
