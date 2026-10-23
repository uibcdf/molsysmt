"""Keeping native elementary-charge values consumable during composition."""

from itertools import permutations

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    MultipleMolecularSystemsError,
    StructuralInconsistencyError,
)
from molsysmt.native import MolecularMechanics, Structures
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol


def test_native_charge_getter_returns_numeric_values_for_public_setters():
    source = declared_methanol()
    values = msm.get(source.molecular_mechanics, element="atom", partial_charge=True)
    assert values.dtype == np.dtype("float64")
    np.testing.assert_allclose(values, [-0.4, -0.5, 0.1, 0.2, 0.3, 0.3])
    output = source.copy()
    msm.set(output, partial_charge=values)
    np.testing.assert_allclose(msm.get(output, partial_charge=True), values)


def test_native_topology_structures_mechanics_compose_with_nondefault_charge_policy():
    source = declared_methanol()
    with msm.pyunitwizard.context(standard_units=["pm", "coulomb"]):
        result = msm.convert(
            [source.topology, source.structures, source.molecular_mechanics],
            to_form="molsysmt.MolSys",
        )
    np.testing.assert_allclose(
        msm.get(result, partial_charge=True), msm.get(source, partial_charge=True)
    )
    assert (
        result.molecular_mechanics.atom_ff_type.tolist()
        == source.molecular_mechanics.atom_ff_type.tolist()
    )
    assert result.chemical_states._states[0].connectivity_completeness == "complete"


@pytest.mark.parametrize("order", list(permutations(range(4))))
def test_four_native_domains_have_order_independent_owners_and_values(order):
    source = declared_methanol()
    domains = (
        source.topology,
        source.chemical_states,
        source.structures,
        source.molecular_mechanics,
    )
    original_states = source.chemical_states
    with msm.pyunitwizard.context(standard_units=["pm", "coulomb"]):
        result = msm.convert([domains[index] for index in order])
    assert result.topology is not source.topology
    assert result.chemical_states is not source.chemical_states
    assert result.structures is not source.structures
    assert result.molecular_mechanics is not source.molecular_mechanics
    assert result.topology._chemical_states_domain is result.chemical_states
    assert source.topology._chemical_states_domain is original_states
    pd.testing.assert_frame_equal(
        result.topology.atoms, source.topology.atoms, check_frame_type=False
    )
    pd.testing.assert_frame_equal(
        result.chemical_states._states[0].bonds,
        source.chemical_states._states[0].bonds,
        check_frame_type=False,
    )
    np.testing.assert_allclose(
        msm.get(result, partial_charge=True), [-0.4, -0.5, 0.1, 0.2, 0.3, 0.3]
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm"),
        np.arange(54).reshape(3, 6, 3) / 10,
    )
    result.chemical_states._states[0].atom_attributes.loc[0, "formal_charge"] = 9
    result.molecular_mechanics.atoms_ff.loc[0, "partial_charge"] = 9.0
    assert (
        source.chemical_states._states[0].atom_attributes.loc[0, "formal_charge"] == 0
    )
    assert source.molecular_mechanics.partial_charge[0] == -0.4


def test_explicit_chemical_domain_owns_states_instead_of_topology_compatibility():
    source = declared_methanol()
    states = source.chemical_states.copy()
    first = states._states[0]
    first.state_id = "explicit-first"
    first.atom_attributes.loc[0, "formal_charge"] = 1
    second = first.copy()
    second.state_id = "explicit-reference"
    second.atom_attributes.loc[0, "formal_charge"] = 2
    second.provenance_index = 12
    states._append_state(second, set_as_reference=True)
    result = msm.convert(
        [source.topology, states, source.structures, source.molecular_mechanics]
    )
    assert result.chemical_states.n_chemical_states == 2
    assert result.chemical_states.reference_chemical_state_index == 1
    assert result.chemical_states._states[1].state_id == "explicit-reference"
    assert result.chemical_states._states[1].provenance_index == 12
    assert (
        result.chemical_states._states[1].atom_attributes.loc[0, "formal_charge"] == 2
    )
    assert pd.isna(result._get_structure_chemical_state_indices()).all()
    assert source.chemical_states.n_chemical_states == 1
    assert (
        source.chemical_states._states[0].atom_attributes.loc[0, "formal_charge"] == 0
    )
    assert states.reference_chemical_state_index == 1


def test_selected_four_domain_composition_uses_existing_native_remapping():
    source = declared_methanol()
    result = msm.convert(
        [
            source.topology,
            source.chemical_states,
            source.structures,
            source.molecular_mechanics,
        ],
        selection=[5, 1, 0],
        structure_indices=[2, 0, 2],
    )
    assert result.topology.atoms.atom_id.tolist() == ["17", "3", "11"]
    np.testing.assert_allclose(msm.get(result, partial_charge=True), [-0.4, -0.5, 0.3])
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm"),
        (np.arange(54).reshape(3, 6, 3) / 10)[[2, 0, 2]][:, [0, 1, 5]],
    )
    assert result.topology.bonds[["atom1_index", "atom2_index"]].values.tolist() == [
        [0, 1],
        [1, 2],
    ]
    assert source.topology.n_atoms == 6 and source.structures.n_structures == 3


@pytest.mark.parametrize("invalid", ["chemistry", "structures", "mechanics"])
def test_full_atom_conflicts_fail_before_selection(invalid):
    source = declared_methanol()
    states, structures, mechanics = (
        source.chemical_states,
        source.structures,
        source.molecular_mechanics,
    )
    if invalid == "chemistry":
        states = states._extract_atoms([0, 1, 2, 3, 4])
    elif invalid == "structures":
        structures = structures.extract(atom_indices=[0, 1, 2, 3, 4])
    else:
        mechanics = mechanics.copy()
        mechanics.atoms_ff = mechanics.atoms_ff.iloc[:5].copy()
    with pytest.raises(StructuralInconsistencyError, match="atom (domain|rows|counts)"):
        msm.convert([source.topology, states, structures, mechanics], selection=[0, 1])


@pytest.mark.parametrize("repeated", [0, 1, 2, 3])
def test_duplicate_explicit_providers_are_rejected(repeated):
    source = declared_methanol()
    domains = [
        source.topology,
        source.chemical_states,
        source.structures,
        source.molecular_mechanics,
    ]
    error = (
        MultipleMolecularSystemsError if repeated == 0 else StructuralInconsistencyError
    )
    with pytest.raises(error):
        msm.convert([*domains, domains[repeated]])


def test_native_mechanics_with_chemical_or_structural_only_domain():
    source = declared_methanol()
    chemical = msm.convert([source.chemical_states, source.molecular_mechanics])
    assert chemical.topology is None and chemical.structures is None
    np.testing.assert_allclose(
        msm.get(chemical, partial_charge=True), [-0.4, -0.5, 0.1, 0.2, 0.3, 0.3]
    )
    structural = msm.convert([source.structures, source.molecular_mechanics])
    assert structural.topology is None and structural.chemical_states is None
    assert structural.structures.n_atoms == 6
    assert len(structural.molecular_mechanics.partial_charge) == 6
    observable = Structures(time=msm.pyunitwizard.quantity([0.0, 1.0], "ps"))
    with pytest.raises(StructuralInconsistencyError, match="atom rows"):
        msm.convert([observable, source.molecular_mechanics])
    parameters = MolecularMechanics()
    parameters.forcefield = "declared_parameters_only"
    result = msm.convert([observable, parameters])
    assert result.topology is None and result._get_n_atoms() is None
    assert result.molecular_mechanics.forcefield == "declared_parameters_only"


def test_explicit_shared_copy_policy_and_empty_chemistry():
    source = declared_methanol()
    result = msm.convert(
        [
            source.topology,
            source.chemical_states,
            source.structures,
            source.molecular_mechanics,
        ],
        copy_if_all=False,
    )
    assert result.structures is not source.structures
    # Structures and Topology already have a live owner and must detach.
    assert result.structures._molsys_owner_ref() is result
    assert result.molecular_mechanics is source.molecular_mechanics
    assert result.topology is not source.topology
    assert result.chemical_states is not source.chemical_states
    source.chemical_states._replace_states([], None)
    empty = msm.convert(
        [
            source.topology,
            source.chemical_states,
            source.structures,
            source.molecular_mechanics,
        ]
    )
    assert empty.chemical_states.n_chemical_states == 0
    assert empty.chemical_states.reference_chemical_state_index is None


def test_full_axis_no_copy_shares_unowned_structures_and_mechanics():
    source = declared_methanol()
    structures = source.structures.copy()
    mechanics = source.molecular_mechanics.copy()
    result = msm.convert(
        [source.topology, source.chemical_states, structures, mechanics],
        copy_if_all=False,
    )
    assert result.structures is structures
    assert result.molecular_mechanics is mechanics
    assert source.structures._molsys_owner_ref() is source


def test_mechanical_parameters_and_named_provenance_survive_without_reassignment():
    source = msm.build.assign_autodock_atom_types(
        declared_methanol(), typing_scheme="autodock4"
    )
    source = msm.build.assign_partial_charges(source, method="gasteiger_marsili")
    source.molecular_mechanics.forcefield = "declared_extra_parameters"
    source.molecular_mechanics.cutoff_distance = msm.pyunitwizard.quantity(
        12.0, "angstrom"
    )
    inputs = [
        source.topology,
        source.chemical_states,
        source.structures,
        source.molecular_mechanics,
    ]
    result = msm.convert(inputs)
    from molsysmt._private.autodock_assignment import (
        validate_assignment as validate_types,
    )
    from molsysmt._private.partial_charges import (
        validate_assignment as validate_charges,
    )

    validate_charges(result)
    validate_types(result, "autodock4")
    for field in ("partial_charge_assignment", "atom_type_assignment"):
        original = getattr(source.molecular_mechanics, field)
        restored = getattr(result.molecular_mechanics, field)
        assert restored is not original
        for key in (
            "schema",
            "method",
            "software",
            "status",
            "chemical_digest",
            "values_digest",
        ):
            if key in original:
                assert restored[key] == original[key]
    selected = msm.convert(inputs, selection=[0, 1, 5])
    validate_charges(selected)
    validate_types(selected, "autodock4")
    np.testing.assert_array_equal(
        selected.molecular_mechanics.partial_charge_assignment["atom_source_indices"],
        [0, 1, 5],
    )
    assert selected.molecular_mechanics.forcefield == "declared_extra_parameters"
    assert float(
        msm.pyunitwizard.get_value(
            selected.molecular_mechanics.cutoff_distance, to_unit="nm"
        )
    ) == pytest.approx(1.2)
    incompatible = source.chemical_states.copy()
    incompatible._states[0].atom_attributes.loc[0, "formal_charge"] = 1
    stale = msm.convert(
        [source.topology, incompatible, source.structures, source.molecular_mechanics],
        selection=[0, 1, 5],
    )
    assert stale.molecular_mechanics.partial_charge_assignment["status"] == "stale"
    assert stale.molecular_mechanics.atom_type_assignment["status"] == "stale"
    with pytest.raises(StructuralInconsistencyError):
        validate_charges(stale)


def test_four_domain_h5msm_preserves_chemistry_and_rejects_nonempty_mechanics(tmp_path):
    source = declared_methanol()
    output = tmp_path / "native.h5msm"
    domains = [
        source.topology,
        source.chemical_states,
        source.structures,
        source.molecular_mechanics,
    ]
    with pytest.raises(ValueError, match="[Mm]echanics"):
        msm.convert(domains, to_form=output)
    assert not output.exists()
    domains[-1] = MolecularMechanics()
    msm.convert(domains, to_form=output, selection=[5, 1, 0], structure_indices=[2, 0])
    restored = msm.convert(output)
    assert restored.topology.atoms.atom_id.tolist() == ["17", "3", "11"]
    assert restored.chemical_states._states[0].connectivity_completeness == "complete"
    assert restored.structures.coordinates.shape == (2, 3, 3)


@pytest.mark.parametrize("observable", [False, True])
def test_absent_structural_atom_axis_is_not_a_declared_zero_length_axis(observable):
    source = declared_methanol()
    structures = (
        Structures(time=msm.pyunitwizard.quantity([0.0, 1.0], "ps"))
        if observable
        else Structures()
    )
    result = msm.convert(
        [
            source.topology,
            source.chemical_states,
            structures,
            source.molecular_mechanics,
        ]
    )
    assert result.get_n_atoms() == 6
    assert result.structures.coordinates is None
    assert result.structures.n_structures == (2 if observable else 0)
    empty_axis = Structures(
        coordinates=msm.pyunitwizard.quantity(np.empty((1, 0, 3)), "nm")
    )
    with pytest.raises(StructuralInconsistencyError, match="atom counts"):
        msm.convert(
            [
                source.topology,
                source.chemical_states,
                empty_axis,
                source.molecular_mechanics,
            ]
        )
