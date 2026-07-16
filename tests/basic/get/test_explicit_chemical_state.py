"""Testing explicit chemical-state resolution across public basic APIs."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Topology


def _build_multistate_topology():
    topology = Topology(n_atoms=3, n_groups=1, n_components=1)
    topology.atoms['atom_id'] = ['0', '1', '2']
    topology.atoms['atom_name'] = ['C1', 'C2', 'O1']
    topology.atoms['atom_type'] = ['C', 'C', 'O']
    topology.atoms['group_index'] = pd.Series([0, 0, 0], dtype='Int64')
    topology.groups['group_id'] = ['0']
    topology.groups['group_name'] = ['LIG']
    topology.groups['group_type'] = ['small molecule']
    topology._set_component_indices([0, 0, 0])
    topology.components['component_id'] = ['reactant']
    topology.components['component_name'] = ['reactant']
    topology.components['component_type'] = ['small molecule']
    topology._set_chemical_state_atom_attribute('formal_charge', [0, 0, -1])
    topology._append_chemical_state_bonds([[0, 1]], orders=1)

    product_index = topology._append_chemical_state(state_id='product')
    product = topology._chemical_states[product_index]
    product.components = topology.components.copy(deep=True)
    product.components.loc[0, 'component_id'] = 'product'
    product.components.loc[0, 'component_name'] = 'product'
    topology._set_component_indices([0, 0, 0], state_index=product_index)
    topology._set_chemical_state_atom_attribute(
        'formal_charge', [1, 0, 0], state_index=product_index
    )
    topology._append_chemical_state_bonds(
        [[0, 2], [1, 2]], orders=[1, 2], state_index=product_index
    )
    topology._set_reference_chemical_state_index(None)
    return topology


def test_get_resolves_atom_component_and_bond_attributes_by_state_index():
    topology = _build_multistate_topology()

    assert msm.get(
        topology, element='atom', chemical_state=0, formal_charge=True
    ) == [0, 0, -1]
    assert msm.get(
        topology, element='atom', chemical_state=1, formal_charge=True
    ) == [1, 0, 0]
    assert msm.get(
        topology, element='component', chemical_state=0, component_name=True
    ) == ['reactant']
    assert msm.get(
        topology, element='component', chemical_state=1, component_name=True
    ) == ['product']
    assert msm.get(
        topology, element='bond', chemical_state=0, bond_order=True
    ) == [1]
    assert msm.get(
        topology, element='bond', chemical_state=1, bond_order=True
    ) == [1, 2]
    assert msm.get(
        topology,
        element='atom',
        chemical_state=1,
        formal_charge=True,
        n_chemical_states=True,
    ) == [[1, 0, 0], 2]


def test_set_and_has_attribute_are_scoped_without_changing_reference_state():
    topology = _build_multistate_topology()
    topology._remove_chemical_state_atom_attribute('stereochemistry', state_index=0)
    topology._set_chemical_state_atom_attribute(
        'stereochemistry', ['R', pd.NA, 'S'], state_index=1
    )

    assert not msm.has_attribute(topology, 'atom_stereochemistry', chemical_state=0)
    assert msm.has_attribute(topology, 'atom_stereochemistry', chemical_state=1)

    msm.set(
        topology,
        element='atom',
        selection=[1],
        chemical_state=1,
        formal_charge=-1,
    )
    msm.set(
        topology,
        element='atom',
        selection='formal_charge==0',
        chemical_state=1,
        atom_is_aromatic=True,
    )

    assert topology._get_chemical_state_atom_attribute(
        'formal_charge', state_index=0
    ).tolist() == [0, 0, -1]
    assert topology._get_chemical_state_atom_attribute(
        'formal_charge', state_index=1
    ).tolist() == [1, -1, 0]
    assert topology._get_chemical_state_atom_attribute(
        'is_aromatic', state_index=1
    ).tolist() == [pd.NA, pd.NA, True]
    assert topology._reference_chemical_state_index is None
    with pytest.raises(StructuralInconsistencyError, match='no reference state'):
        msm.get(topology, element='atom', formal_charge=True)


def test_select_uses_the_requested_state_for_chemistry_and_components():
    topology = _build_multistate_topology()

    assert msm.select(topology, 'formal_charge==-1', chemical_state=0) == [2]
    assert msm.select(topology, 'formal_charge==1', chemical_state=1) == [0]
    assert msm.select(
        topology, 'component_name=="reactant"', chemical_state=0
    ) == [0, 1, 2]
    assert msm.select(
        topology, 'component_name=="product"', chemical_state=1
    ) == [0, 1, 2]
    assert msm.select(
        topology,
        'atom_index==0 bonded to atom_index==1',
        chemical_state=0,
    ) == [0]
    assert msm.select(
        topology,
        'atom_index==0 bonded to atom_index==1',
        chemical_state=1,
    ) == []


def test_molsys_selection_reuses_its_context_scoped_native_topology():
    molsys = MolSys()
    molsys.topology = _build_multistate_topology()

    assert msm.select(molsys, 'formal_charge==1', chemical_state=1) == [0]
    assert molsys.topology._reference_chemical_state_index is None


@pytest.mark.parametrize('chemical_state', [-1, True, 'product'])
def test_chemical_state_argument_rejects_ambiguous_or_invalid_selectors(chemical_state):
    topology = _build_multistate_topology()

    with pytest.raises(ArgumentError):
        msm.get(
            topology,
            element='atom',
            chemical_state=chemical_state,
            formal_charge=True,
        )


def test_out_of_range_state_does_not_leak_context():
    topology = _build_multistate_topology()

    with pytest.raises(StructuralInconsistencyError, match='index 2 is invalid'):
        msm.get(topology, element='atom', chemical_state=2, formal_charge=True)
    with pytest.raises(StructuralInconsistencyError, match='no reference state'):
        msm.get(topology, element='atom', formal_charge=True)


def test_explicit_state_predicates_reject_non_native_selection_syntaxes():
    topology = _build_multistate_topology()

    with pytest.raises(ArgumentError):
        msm.select(
            topology,
            'name C1',
            chemical_state=1,
            syntax='MDTraj',
        )
