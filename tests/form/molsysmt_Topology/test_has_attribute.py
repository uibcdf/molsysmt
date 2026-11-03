"""Testing instance-aware presence for optional native topology attributes."""

import pytest

import molsysmt as msm
from molsysmt.native import Topology


@pytest.mark.parametrize(
    "attribute",
    [
        "isotope",
        "formal_charge",
        "chemical_state_id",
        "component_index",
        "component_id",
        "component_name",
        "component_type",
        "bond_id",
        "fractional_bond_order",
        "bond_is_aromatic",
    ],
)
def test_unmaterialized_topology_attributes_are_not_present(attribute):
    topology = Topology(n_atoms=2, skip_digestion=True)

    assert msm.has_attribute(topology, attribute, include_none=True) == (
        attribute == "isotope"
    )
    assert not msm.has_attribute(topology, attribute)


@pytest.mark.parametrize(
    "attribute",
    [
        "n_atoms",
        "n_groups",
        "n_components",
        "n_bonds",
        "n_chemical_states",
        "chemical_state_index",
        "reference_chemical_state_index",
        "connectivity_completeness",
        "component_completeness",
        "component_evidence",
    ],
)
def test_derived_and_explicit_state_metadata_are_available(attribute):
    topology = Topology(n_atoms=2, skip_digestion=True)

    assert msm.has_attribute(topology, attribute) == (
        attribute in {"n_atoms", "n_groups"}
    )


def test_materialized_state_id_and_component_are_present():
    from molsysmt.native import MolSys

    system = MolSys(n_atoms=2, n_components=1)
    system.chemical_states._states[0].state_id = "reactant"
    system.chemical_states._set_component_indices([0, 0])
    system.chemical_states._states[0].components.loc[0] = [
        "part",
        "Part",
        "small molecule",
    ]
    for attribute in (
        "chemical_state_id",
        "component_index",
        "component_id",
        "component_name",
        "component_type",
    ):
        assert msm.has_attribute(system, attribute)
        assert not msm.has_attribute(system.topology, attribute, include_none=True)
