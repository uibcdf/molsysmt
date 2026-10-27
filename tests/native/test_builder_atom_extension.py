"""Owned atom-domain growth preserves evidence and refuses invalid edits atomically."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm


def source():
    from rdkit import Chem

    return msm.convert(Chem.MolFromSmiles("CCO"), to_form="molsysmt.MolSys")


def snapshot(builder):
    domain = builder.topology._chemical_states_domain
    return (
        builder.topology.atoms.copy(deep=True),
        domain.n_atoms,
        [
            (
                state.atom_attributes.copy(deep=True),
                state.component_indices.copy(deep=True),
                deepcopy(state.bonds),
                state.connectivity_completeness,
                state.component_completeness,
            )
            for state in domain._states
        ],
    )


def assert_unchanged(builder, before):
    atoms, n_atoms, states = before
    pd.testing.assert_frame_equal(atoms, builder.topology.atoms)
    assert builder.topology._chemical_states_domain.n_atoms == n_atoms
    for state, (attrs, components, bonds, covalent, component) in zip(
        builder.topology._chemical_states_domain._states, states
    ):
        pd.testing.assert_frame_equal(attrs, state.atom_attributes)
        pd.testing.assert_series_equal(components, state.component_indices)
        pd.testing.assert_frame_equal(pd.DataFrame(bonds), pd.DataFrame(state.bonds))
        assert state.connectivity_completeness == covalent
        assert state.component_completeness == component


@pytest.mark.parametrize("n_states", [1, 2, 3])
def test_atom_extension_aligns_every_state_and_preserves_existing_evidence(n_states):
    molsys = source()
    for i in range(1, n_states):
        state = deepcopy(molsys.chemical_states._states[0])
        state.state_id = f"variant-{i}"
        state.atom_attributes.loc[0, "formal_charge"] = i
        molsys.chemical_states._append_state(state, False)
    if n_states > 1:
        molsys.chemical_states._set_reference_index(n_states - 1)
    for i, state in enumerate(molsys.chemical_states._states):
        state.provenance_index = 0
        state._preparation_history = [
            {
                "schema": "molsysmt.preparation_record@1",
                "index_scope": "operation",
                "output": {"n_atoms": 3, "n_bonds": 2, "chemical_state_index": i},
                "report": {
                    "schema": "tests.builder_seed@1",
                    "producer_version": "original-1",
                },
            }
        ]
    original = deepcopy(molsys.chemical_states)
    builder = msm.MolSysBuilder(molsys)
    states = builder.topology._chemical_states_domain._states
    before = [
        (
            s.atom_attributes.copy(deep=True),
            s.component_indices.copy(deep=True),
            s.bonds,
            s.components,
            s.state_id,
            s.provenance_index,
            deepcopy(s._preparation_history),
        )
        for s in states
    ]
    assert builder.add_atom(atom_id=97, atom_name="Ar", atom_type="Ar") == 3
    domain = builder.topology._chemical_states_domain
    assert domain.n_atoms == 4
    assert domain.reference_chemical_state_index == n_states - 1
    assert builder.topology.atoms.atom_id.tolist() == ["0", "1", "2", "97"]
    for state, (attrs, components, bonds, table, label, provenance, history) in zip(
        domain._states, before
    ):
        pd.testing.assert_frame_equal(attrs, state.atom_attributes.iloc[:3])
        pd.testing.assert_series_equal(components, state.component_indices.iloc[:3])
        assert state.atom_attributes.iloc[3].isna().all()
        assert pd.isna(state.component_indices.iloc[3])
        assert state.bonds is bonds and state.components is table
        assert state.state_id == label and state.provenance_index == provenance
        assert state._preparation_history == history
        assert state.connectivity_completeness == "partial"
        for field, dtype in attrs.dtypes.items():
            assert state.atom_attributes[field].dtype == dtype
    assert molsys.topology.n_atoms == 3
    for actual, expected in zip(molsys.chemical_states._states, original._states):
        pd.testing.assert_frame_equal(actual.atom_attributes, expected.atom_attributes)
        pd.testing.assert_series_equal(
            actual.component_indices, expected.component_indices
        )


@pytest.mark.parametrize(
    "corruption",
    [
        "attribute_rows",
        "component_rows",
        "unknown_column",
        "invalid_values",
        "domain_count",
        "attribute_index",
        "stable_index",
        "completeness",
    ],
)
def test_malformed_later_state_rejects_before_any_inventory_changes(corruption):
    builder = msm.MolSysBuilder(source())
    domain = builder.topology._chemical_states_domain
    domain._append_state(deepcopy(domain._states[0]), False)
    state = domain._states[1]
    if corruption == "attribute_rows":
        state.atom_attributes = state.atom_attributes.iloc[:2].copy()
    elif corruption == "component_rows":
        state.component_indices = state.component_indices.iloc[:2].copy()
    elif corruption == "unknown_column":
        state.atom_attributes["unsupported"] = 1
    elif corruption == "invalid_values":
        state.atom_attributes["stereochemistry"] = ["bad"] * 3
    elif corruption == "domain_count":
        domain._n_atoms = 2
    elif corruption == "attribute_index":
        state.atom_attributes.index = [1, 2, 3]
    elif corruption == "stable_index":
        builder.topology.atoms.index = [1, 2, 3]
    elif corruption == "completeness":
        state._connectivity_completeness = "invalid"
    before = snapshot(builder)
    with pytest.raises(msm.StructuralInconsistencyError):
        builder.add_atom(atom_name="Ar", atom_type="Ar")
    assert_unchanged(builder, before)


@pytest.mark.parametrize("attribute", ["coordinates", "velocities", "b_factor"])
def test_existing_atom_dependent_structure_arrays_reject_without_mutation(attribute):
    builder = msm.MolSysBuilder(source())
    if attribute == "b_factor":
        value = msm.pyunitwizard.quantity(np.ones((1, 3)), "nm**2")
    else:
        value = msm.pyunitwizard.quantity(
            np.zeros((1, 3, 3)), "nm" if attribute == "coordinates" else "nm/ps"
        )
    setattr(builder.structures, attribute, value)
    before = snapshot(builder)
    with pytest.raises(msm.StructuralInconsistencyError, match="Atoms cannot be added"):
        builder.add_atom(atom_name="Ar", atom_type="Ar")
    assert_unchanged(builder, before)


def test_failed_atom_name_resolution_does_not_append_a_partial_atom(monkeypatch):
    builder = msm.MolSysBuilder(source())
    before = snapshot(builder)

    def fail(*args, **kwargs):
        raise RuntimeError("controlled type resolution failure")

    monkeypatch.setattr(msm.element.atom, "get_atom_type_from_atom_name", fail)
    with pytest.raises(RuntimeError, match="controlled type resolution failure"):
        builder.add_atom(atom_name="new")
    assert_unchanged(builder, before)


def test_strict_resize_validation_is_not_relaxed_for_unaligned_state_growth():
    states = source().chemical_states
    before = states.n_atoms
    with pytest.raises(msm.StructuralInconsistencyError):
        states._resize_atom_domain(before + 1)
    assert states.n_atoms == before
    assert len(states._states[0].atom_attributes) == before


def test_fresh_builder_addition_does_not_invent_chemical_columns():
    builder = msm.MolSysBuilder()
    for i in range(3):
        builder.add_atom(atom_id=i, atom_name="C", atom_type="C")
    state = builder.topology._chemical_states_domain._states[0]
    assert state.atom_attributes.shape == (3, 0)
    assert state.component_indices.isna().all()
    assert state.connectivity_completeness == "unavailable"


def test_preparation_allocation_failure_in_later_state_leaves_owned_tables_untouched(
    monkeypatch,
):
    from molsysmt.native.topology import _ChemicalStateStorage

    builder = msm.MolSysBuilder(source())
    domain = builder.topology._chemical_states_domain
    domain._append_state(deepcopy(domain._states[0]), False)
    before = snapshot(builder)
    originals = [(s.atom_attributes, s.component_indices) for s in domain._states]
    original = _ChemicalStateStorage._validated_atom_attributes
    calls = []

    def fail_later(cls, table):
        calls.append(1)
        if len(calls) == 2:
            raise MemoryError("controlled allocation failure")
        return original(table)

    monkeypatch.setattr(
        _ChemicalStateStorage, "_validated_atom_attributes", classmethod(fail_later)
    )
    with pytest.raises(MemoryError, match="controlled allocation failure"):
        builder.add_atom(atom_name="Ar", atom_type="Ar")
    assert_unchanged(builder, before)
    for state, (attrs, components) in zip(domain._states, originals):
        assert state.atom_attributes is attrs and state.component_indices is components


def test_atom_growth_does_not_choose_an_ambiguous_reference():
    builder = msm.MolSysBuilder(source())
    domain = builder.topology._chemical_states_domain
    domain._append_state(deepcopy(domain._states[0]), False)
    domain._set_reference_index(None)
    assert builder.add_atom(atom_name="Ar", atom_type="Ar") == 3
    assert domain.reference_chemical_state_index is None
    assert [len(s.atom_attributes) for s in domain._states] == [4, 4]


@pytest.mark.parametrize("permuted", [False, True])
def test_group_free_build_grows_molecule_inventory_without_inventing_groups(permuted):
    from rdkit import Chem

    molsys = msm.convert(Chem.MolFromSmiles("CCO.COC"), to_form="molsysmt.MolSys")
    molsys.topology.molecules["molecule_id"] = pd.Series(
        ["ethanol", "ether"], dtype="string"
    )
    if permuted:
        molsys = msm.permute_atoms(molsys, atom_indices=[3, 4, 5, 0, 1, 2])
    builder = msm.MolSysBuilder(molsys)
    builder.add_atom(atom_name="Ar", atom_type="Ar")
    result = builder.build()
    assert result.topology.n_groups == 0
    assert result.topology.n_molecules == 3
    assert result.topology.molecules.molecule_id.tolist()[:2] == ["ethanol", "ether"]
    expected = [[3, 4, 5], [0, 1, 2], [6]] if permuted else [[0, 1, 2], [3, 4, 5], [6]]
    assert msm.get(result, element="molecule", atom_index=True) == expected
    assert result.chemical_states.n_atoms == 7
    assert result.chemical_states._states[0].atom_attributes.iloc[-1].isna().all()


def test_new_bonded_atom_keeps_the_inherited_group_free_molecule_axis():
    builder = msm.MolSysBuilder(source())
    builder.add_atom(atom_name="C", atom_type="C")
    builder.add_bond(2, 3, bond_order=1, bond_type="covalent")
    result = builder.build()
    assert result.topology.n_groups == 0 and result.topology.n_molecules == 1
    assert msm.get(result, element="molecule", atom_index=True) == [[0, 1, 2, 3]]
    assert result.chemical_states._states[0].connectivity_completeness == "partial"


def test_inherited_group_free_molecule_merge_requires_explicit_group_boundaries():
    from rdkit import Chem

    molsys = msm.convert(Chem.MolFromSmiles("CCO.COC"), to_form="molsysmt.MolSys")
    builder = msm.MolSysBuilder(molsys)
    builder.add_atom(atom_name="C", atom_type="C")
    builder.add_bond(1, 6, bond_order=1, bond_type="covalent")
    builder.add_bond(4, 6, bond_order=1, bond_type="covalent")
    with pytest.raises(
        msm.StructuralInconsistencyError, match="declare explicit groups"
    ):
        builder.build()
    assert builder.n_atoms == 7 and builder.n_groups == 0
    builder.add_group([0, 1, 2, 6], group_name="LIG")
    builder.add_group([3, 4, 5], group_name="LIG")
    result = builder.build()
    assert result.topology.n_molecules == 2
    assert msm.get(result, element="molecule", atom_index=True) == [
        [0, 1, 2, 6],
        [3, 4, 5],
    ]


def test_extended_unknown_state_round_trips_through_public_h5msm(tmp_path):
    builder = msm.MolSysBuilder(source())
    builder.add_atom(atom_name="Ar", atom_type="Ar")
    result = builder.build()
    path = msm.convert(result, to_form=str(tmp_path / "extended.h5msm"))
    recovered = msm.convert(path, to_form="molsysmt.MolSys")
    assert recovered.topology.n_atoms == 4 and recovered.chemical_states.n_atoms == 4
    assert recovered.topology.n_groups == 0 and recovered.topology.n_molecules == 2
    assert recovered.chemical_states._states[0].atom_attributes.iloc[-1].isna().all()
    assert recovered.chemical_states._states[0].connectivity_completeness == "partial"
    assert msm.get(recovered, element="molecule", atom_index=True) == [[0, 1, 2], [3]]
