"""Checking declared composition of chemical and structural index domains."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import MolSys


@pytest.fixture
def domains():
    system = MolSys(n_atoms=4)
    system.topology.add_bonds([[0, 1], [2, 3]])
    msm.set(system.topology, element="atom", formal_charge=[0, 1, -1, 0])
    first = system.chemical_states._states[0]
    first.state_id = "neutral-reference"
    first.connectivity_completeness = "complete"
    second = first.copy()
    second.state_id = "charged-reference"
    second.atom_attributes["formal_charge"] = pd.array([1, 0, 0, -1], dtype="Int64")
    second.provenance_index = 12
    system.chemical_states._append_state(second, set_as_reference=True)
    system.structures.append(
        coordinates=puw.quantity(np.arange(36).reshape(3, 4, 3), "angstrom"),
        box=puw.quantity(np.repeat((np.eye(3) * 20)[None], 3, axis=0), "angstrom"),
        time=puw.quantity([0, 1000, 2000], "fs"),
    )
    system.structures.structure_id = np.array(["frame-a", "frame-b", "frame-c"])
    return system.chemical_states, system.structures


def _source(states, structures, dictionary, reverse):
    chemistry = msm.convert(states, to_form="molsysmt.ChemicalStatesDict") if dictionary else states
    return [structures, chemistry] if reverse else [chemistry, structures]


@pytest.mark.parametrize("dictionary", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_compose_chemical_and_structural_domains_without_inventing_topology(domains, dictionary, reverse):
    states, structures = domains
    result = msm.convert(_source(states, structures, dictionary, reverse), to_form="molsysmt.MolSys")
    assert result.topology is None and not result.interactions
    assert msm.get(result, n_atoms=True, n_structures=True) == [4, 3]
    assert result.chemical_states.n_chemical_states == 2
    assert result.chemical_states.reference_chemical_state_index == 1
    assert result.chemical_states is not states and result.structures is not structures
    assert result._structure_chemical_state_indices is None
    assert pd.isna(result._get_structure_chemical_state_indices()).all()
    for actual, expected in zip(result.chemical_states._states, states._states):
        pd.testing.assert_frame_equal(actual.atom_attributes, expected.atom_attributes)
        pd.testing.assert_frame_equal(actual.bonds, expected.bonds, check_frame_type=False)
        assert actual.state_id == expected.state_id
        assert actual.provenance_index == expected.provenance_index
        assert actual.connectivity_completeness == "complete"
    assert puw.get_unit(result.structures.coordinates) == puw.unit("nm")
    assert puw.get_unit(result.structures.time) == puw.unit("ps")
    np.testing.assert_allclose(puw.get_value(result.structures.coordinates, to_unit="nm"),
                               np.arange(36).reshape(3, 4, 3) * .1, atol=1e-12, rtol=0)
    # The default result owns its domains, so editing it leaves both inputs intact.
    result.chemical_states._states[1].atom_attributes.loc[0, "formal_charge"] = 99
    result.structures.set_box(value=puw.quantity(np.repeat((np.eye(3) * 3)[None], 3, axis=0), "nm"))
    assert states._states[1].atom_attributes.loc[0, "formal_charge"] == 1
    np.testing.assert_allclose(puw.get_value(structures.box, to_unit="nm"),
                               np.repeat((np.eye(3) * 2)[None], 3, axis=0), atol=1e-12, rtol=0)


@pytest.mark.parametrize("dictionary", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_selected_composition_remaps_bonds_charges_and_frames_in_requested_order(domains, dictionary, reverse):
    states, structures = domains
    with puw.context(standard_units=["angstrom", "fs", "degree"]):
        result = msm.convert(_source(states, structures, dictionary, reverse),
                             selection=[3, 2, 0], structure_indices=[2, 0, 2])
    assert result.topology is None
    assert result.chemical_states.n_atoms == 3
    assert result.chemical_states.reference_chemical_state_index == 1
    for state in result.chemical_states._states:
        assert state.bonds[["atom1_index", "atom2_index"]].to_numpy().tolist() == [[0, 1]]
    assert result.chemical_states._states[1].atom_attributes.formal_charge.tolist() == [-1, 0, 1]
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        (np.arange(36).reshape(3, 4, 3) * .1)[[2, 0, 2]][:, [3, 2, 0]], atol=1e-12, rtol=0,
    )
    np.testing.assert_array_equal(puw.get_value(result.structures.time, to_unit="ps"), [2, 0, 2])
    assert result.structures.structure_id.tolist() == ["frame-c", "frame-a", "frame-c"]
    assert pd.isna(result._get_structure_chemical_state_indices()).all()
    assert states.n_atoms == 4 and structures.n_atoms == 4


@pytest.mark.parametrize("dictionary", [False, True])
def test_incompatible_full_atom_axes_fail_before_a_selection_can_hide_them(domains, dictionary):
    states, structures = domains
    shorter = structures.extract(atom_indices=[0, 1, 2])
    with pytest.raises(StructuralInconsistencyError, match="atom (counts|domain)"):
        msm.convert(_source(states, shorter, dictionary, False), selection=[0, 1])


def test_copy_policy_and_single_state_implicit_association(domains):
    states, structures = domains
    single = states.copy()
    single._replace_states([single._states[0]], reference_index=0)
    result = msm.convert([single, structures], copy_if_all=False)
    assert result.chemical_states is single and result.structures is structures
    assert result._structure_chemical_state_indices is None
    assert result._get_structure_chemical_state_indices().tolist() == [0, 0, 0]
    selected = msm.convert([single, structures], selection=[1, 0], copy_if_all=False)
    assert selected.chemical_states is not single and selected.structures is not structures


def test_composed_domains_persist_through_public_h5msm_conversion(domains, tmp_path):
    states, structures = domains
    path = str(tmp_path / "domains.h5msm")
    msm.convert([states, structures], to_form=path, selection=[3, 2, 0], structure_indices=[2, 0])
    restored = msm.convert(path)
    assert restored.topology is None
    assert restored.chemical_states.reference_chemical_state_index == 1
    assert restored.chemical_states._states[1].state_id == "charged-reference"
    assert restored.chemical_states._states[1].atom_attributes.formal_charge.tolist() == [-1, 0, 1]
    np.testing.assert_array_equal(puw.get_value(restored.structures.time, to_unit="ps"), [2, 0])
    assert pd.isna(restored._get_structure_chemical_state_indices()).all()
