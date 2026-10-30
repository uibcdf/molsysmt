"""Testing explicit chemical-state resolution across public basic APIs."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys


def _build_multistate_molsys():
    topology = MolSys(n_atoms=3, n_groups=1, n_components=1)
    topology.topology.atoms["atom_id"] = ["0", "1", "2"]
    topology.topology.atoms["atom_name"] = ["C1", "C2", "O1"]
    topology.topology.atoms["atom_type"] = ["C", "C", "O"]
    topology.topology.atoms["group_index"] = pd.Series([0, 0, 0], dtype="Int64")
    topology.topology.groups["group_id"] = ["0"]
    topology.topology.groups["group_name"] = ["LIG"]
    topology.topology.groups["group_type"] = ["small molecule"]
    topology.chemical_states._set_component_indices([0, 0, 0])
    topology.chemical_states._states[0].components["component_id"] = ["reactant"]
    topology.chemical_states._states[0].components["component_name"] = ["reactant"]
    topology.chemical_states._states[0].components["component_type"] = [
        "small molecule"
    ]
    topology.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0, 0, -1]
    )
    topology.chemical_states._append_chemical_state_bonds([[0, 1]], orders=1)

    product_index = topology.chemical_states.append_state()
    topology.chemical_states._states[product_index].state_id = "product"
    product = topology.chemical_states._states[product_index]
    product.components = topology.chemical_states._states[0].components.copy(deep=True)
    product.components.loc[0, "component_id"] = "product"
    product.components.loc[0, "component_name"] = "product"
    topology.chemical_states._set_component_indices(
        [0, 0, 0], state_index=product_index
    )
    topology.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [1, 0, 0], state_index=product_index
    )
    topology.chemical_states._append_chemical_state_bonds(
        [[0, 2], [1, 2]], orders=[1, 2], state_index=product_index
    )
    topology.chemical_states._set_reference_index(None)
    return topology


def test_get_resolves_atom_component_and_bond_attributes_by_state_index():
    topology = _build_multistate_molsys()

    assert msm.get(topology, element="atom", chemical_state=0, formal_charge=True) == [
        0,
        0,
        -1,
    ]
    assert msm.get(topology, element="atom", chemical_state=1, formal_charge=True) == [
        1,
        0,
        0,
    ]
    assert msm.get(
        topology, element="component", chemical_state=0, component_name=True
    ) == ["reactant"]
    assert msm.get(
        topology, element="component", chemical_state=1, component_name=True
    ) == ["product"]
    assert msm.get(topology, element="bond", chemical_state=0, bond_order=True) == [1]
    assert msm.get(topology, element="bond", chemical_state=1, bond_order=True) == [
        1,
        2,
    ]
    assert msm.get(
        topology,
        element="atom",
        chemical_state=1,
        formal_charge=True,
        n_chemical_states=True,
    ) == [[1, 0, 0], 2]


def test_set_and_has_attribute_are_scoped_without_changing_reference_state():
    topology = _build_multistate_molsys()
    topology.chemical_states._remove_chemical_state_atom_attribute(
        "stereochemistry", state_index=0
    )
    topology.chemical_states._set_chemical_state_atom_attribute(
        "stereochemistry", ["R", pd.NA, "S"], state_index=1
    )

    assert not msm.has_attribute(topology, "atom_stereochemistry", chemical_state=0)
    assert msm.has_attribute(topology, "atom_stereochemistry", chemical_state=1)

    msm.set(
        topology,
        element="atom",
        selection=[1],
        chemical_state=1,
        formal_charge=-1,
    )
    msm.set(
        topology,
        element="atom",
        selection="formal_charge==0",
        chemical_state=1,
        atom_is_aromatic=True,
    )

    assert topology.chemical_states._get_chemical_state_atom_attribute(
        "formal_charge", state_index=0
    ).tolist() == [0, 0, -1]
    assert topology.chemical_states._get_chemical_state_atom_attribute(
        "formal_charge", state_index=1
    ).tolist() == [1, -1, 0]
    assert topology.chemical_states._get_chemical_state_atom_attribute(
        "is_aromatic", state_index=1
    ).tolist() == [pd.NA, pd.NA, True]
    assert topology.chemical_states.reference_chemical_state_index is None
    with pytest.raises(StructuralInconsistencyError, match="no reference state"):
        msm.get(topology, element="atom", formal_charge=True)


def test_select_uses_the_requested_state_for_chemistry_and_components():
    topology = _build_multistate_molsys()

    assert msm.select(topology, "formal_charge==-1", chemical_state=0) == [2]
    assert msm.select(topology, "formal_charge==1", chemical_state=1) == [0]
    assert msm.select(topology, 'component_name=="reactant"', chemical_state=0) == [
        0,
        1,
        2,
    ]
    assert msm.select(topology, 'component_name=="product"', chemical_state=1) == [
        0,
        1,
        2,
    ]
    assert msm.select(
        topology,
        "atom_index==0 bonded to atom_index==1",
        chemical_state=0,
    ) == [0]
    assert (
        msm.select(
            topology,
            "atom_index==0 bonded to atom_index==1",
            chemical_state=1,
        )
        == []
    )


def test_molsys_selection_reuses_its_context_scoped_native_topology():
    molsys = _build_multistate_molsys()

    assert msm.select(molsys, "formal_charge==1", chemical_state=1) == [0]
    assert molsys.chemical_states.reference_chemical_state_index is None


@pytest.mark.parametrize("chemical_state", [-1, True, "product"])
def test_chemical_state_argument_rejects_ambiguous_or_invalid_selectors(chemical_state):
    topology = _build_multistate_molsys()

    with pytest.raises(ArgumentError):
        msm.get(
            topology,
            element="atom",
            chemical_state=chemical_state,
            formal_charge=True,
        )


def test_out_of_range_state_does_not_leak_context():
    topology = _build_multistate_molsys()

    with pytest.raises(StructuralInconsistencyError, match="index 2 is invalid"):
        msm.get(topology, element="atom", chemical_state=2, formal_charge=True)
    with pytest.raises(StructuralInconsistencyError, match="no reference state"):
        msm.get(topology, element="atom", formal_charge=True)


def test_explicit_state_predicates_reject_non_native_selection_syntaxes():
    topology = _build_multistate_molsys()

    with pytest.raises(ArgumentError):
        msm.select(
            topology,
            "name C1",
            chemical_state=1,
            syntax="MDTraj",
        )


def test_composed_native_queries_borrow_domains_without_copying_or_rebinding(
    monkeypatch,
):
    """Component-to-molecule projection must use both independent authorities."""
    import numpy as np

    from molsysmt.native import ChemicalStates, Structures, Topology

    source = MolSys(n_atoms=3, n_molecules=2)
    source.topology.set_atom_molecules([0, 0, 1])
    source.chemical_states.add_bonds([[0, 1], [1, 2]])
    source.chemical_states.append_state()
    source.chemical_states.add_bonds([[0, 1]], chemical_state=1)
    source.structures.coordinates = msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm")
    domains = [source.topology, source.chemical_states, source.structures]
    coordinates = source.structures.coordinates
    reference = source.chemical_states.reference_chemical_state_index

    def forbid(*args, **kwargs):
        raise AssertionError("A composed native query must not copy its domains.")

    for cls in (Topology, ChemicalStates, Structures):
        monkeypatch.setattr(cls, "copy", forbid)
        monkeypatch.setattr(cls, "__deepcopy__", forbid)

    assert msm.get(
        domains, element="component", chemical_state=0, molecule_index=True
    ) == [[0, 1]]
    assert msm.get(
        domains, element="component", chemical_state=1, molecule_index=True
    ) == [0, 1]
    for domain in domains:
        assert domain._molsys_owner_ref() is source
    assert source.chemical_states.reference_chemical_state_index == reference
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates),
        msm.pyunitwizard.get_value(coordinates),
    )
