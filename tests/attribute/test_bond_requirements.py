"""Keep stored stable inventory independent from state-local graph requirements."""

import pytest

import molsysmt as msm
from molsysmt.attribute import bonds_are_required_to_get_attribute
from molsysmt.native import Topology

STABLE_ATTRIBUTES = (
    "atom_index",
    "group_index",
    "chain_index",
    "chain_type",
    "molecule_index",
    "molecule_id",
    "molecule_name",
    "molecule_type",
    "entity_index",
    "entity_id",
    "entity_name",
    "entity_type",
    "n_atoms",
    "n_groups",
    "n_chains",
    "n_molecules",
    "n_entities",
    "n_peptides",
    "n_proteins",
    "n_dnas",
    "n_rnas",
    "n_waters",
)
STABLE_ELEMENTS = (None, "system", "atom", "group", "chain", "molecule", "entity")
GRAPH_ATTRIBUTES = (
    "component_index",
    "component_id",
    "component_name",
    "component_type",
    "n_components",
    "bond_index",
    "bond_id",
    "bond_type",
    "bond_order",
    "bond_is_aromatic",
    "bonded_atoms",
    "bonded_atom_pairs",
    "inner_bond_index",
    "inner_bonded_atoms",
    "inner_bonded_atom_pairs",
    "n_bonds",
    "n_inner_bonds",
)


@pytest.mark.parametrize("attribute", STABLE_ATTRIBUTES)
@pytest.mark.parametrize("from_element", STABLE_ELEMENTS)
def test_stored_inventory_does_not_require_bonds(attribute, from_element):
    assert bonds_are_required_to_get_attribute(attribute, from_element) is False


@pytest.mark.parametrize("attribute", GRAPH_ATTRIBUTES)
@pytest.mark.parametrize("from_element", STABLE_ELEMENTS)
def test_graph_attributes_still_require_bonds(attribute, from_element):
    assert bonds_are_required_to_get_attribute(attribute, from_element) is True


@pytest.mark.parametrize("attribute", STABLE_ATTRIBUTES)
@pytest.mark.parametrize("from_element", ("component", "bond"))
def test_projecting_from_a_state_local_axis_still_requires_its_graph(
    attribute, from_element
):
    assert bonds_are_required_to_get_attribute(attribute, from_element) is True


@pytest.mark.parametrize("domain", ("topology", "absent", "zero_states"))
def test_stored_membership_queries_and_selections_need_no_chemical_state(domain):
    topology = Topology(n_atoms=4, n_groups=2, n_chains=2, n_molecules=2, n_entities=2)
    topology.atoms["group_index"] = [0, 0, 1, 1]
    topology.atoms["chain_index"] = [0, 0, 1, 1]
    topology.groups["molecule_index"] = [0, 1]
    topology.molecules["molecule_id"] = ["pep", "wat"]
    topology.molecules["entity_index"] = [0, 1]
    if domain == "topology":
        molsys = topology
    else:
        molsys = msm.convert(topology, to_form="molsysmt.MolSys")
        if domain == "zero_states":
            molsys.chemical_states = msm.ChemicalStates(n_atoms=4)
            assert molsys.chemical_states.n_chemical_states == 0
        else:
            assert molsys.chemical_states is None

    assert msm.get(molsys, element="atom", molecule_index=True) == [0, 0, 1, 1]
    assert msm.get(molsys, element="atom", molecule_id=True) == [
        "pep",
        "pep",
        "wat",
        "wat",
    ]
    assert msm.get(molsys, element="atom", entity_index=True) == [0, 0, 1, 1]
    assert msm.get(molsys, element="molecule", atom_index=True) == [[0, 1], [2, 3]]
    assert msm.select(molsys, selection="molecule_id == 'wat'") == [2, 3]
    assert msm.select(molsys, selection="entity_index == 0") == [0, 1]
