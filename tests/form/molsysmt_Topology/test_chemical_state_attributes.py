import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import MolSys, MolecularMechanics, Topology
from molsysmt.attribute import attributes, is_chemical_state_attribute


def test_registry_classifies_the_complete_first_atom_state_vertical():
    expected = {
        'formal_charge': ('Int16', 'elementary_charge'),
        'atom_is_aromatic': ('boolean', None),
        'n_unpaired_electrons': ('UInt8', None),
        'n_implicit_hydrogens': ('UInt8', None),
        'allows_implicit_hydrogens': ('boolean', None),
        'atom_stereochemistry': ('string', None),
    }

    for attribute, (dtype, units) in expected.items():
        assert is_chemical_state_attribute(attribute)
        assert not attributes[attribute]['topological']
        assert not attributes[attribute]['mechanical']
        assert attributes[attribute]['domain'] == 'atom'
        assert attributes[attribute]['dtype'] == dtype
        assert attributes[attribute]['nullable'] is True
        assert attributes[attribute]['units'] == units


def test_public_atom_state_get_set_and_nullable_values():
    topology = Topology(n_atoms=3)

    msm.set(
        topology,
        element='atom',
        formal_charge=[0, -1, 1],
        atom_is_aromatic=[False, True, None],
        n_unpaired_electrons=[0, 1, None],
        n_implicit_hydrogens=[3, 0, None],
        allows_implicit_hydrogens=[True, False, None],
        atom_stereochemistry=['unspecified', 'R', None],
    )

    observed = msm.get(
        topology,
        element='atom',
        output_type='dictionary',
        formal_charge=True,
        atom_is_aromatic=True,
        n_unpaired_electrons=True,
        n_implicit_hydrogens=True,
        allows_implicit_hydrogens=True,
        atom_stereochemistry=True,
    )

    assert observed['formal_charge'] == [0, -1, 1]
    assert observed['atom_is_aromatic'] == [False, True, pd.NA]
    assert observed['n_unpaired_electrons'] == [0, 1, pd.NA]
    assert observed['n_implicit_hydrogens'] == [3, 0, pd.NA]
    assert observed['allows_implicit_hydrogens'] == [True, False, pd.NA]
    assert observed['atom_stereochemistry'] == ['unspecified', 'R', pd.NA]

    copy = Topology(n_atoms=3)
    msm.set(copy, element='atom', **observed)
    copied = msm.get(
        copy, element='atom', output_type='dictionary',
        formal_charge=True, atom_is_aromatic=True,
        n_unpaired_electrons=True, n_implicit_hydrogens=True,
        allows_implicit_hydrogens=True, atom_stereochemistry=True,
    )
    assert copied == observed


def test_formal_charge_accepts_elementary_charge_quantity_and_partial_selection():
    topology = Topology(n_atoms=3)
    charges = puw.quantity([0, -1, 1], 'elementary_charge')

    msm.set(topology, element='atom', formal_charge=charges)
    msm.set(topology, element='atom', selection=[1], formal_charge=0)

    assert msm.get(topology, element='atom', formal_charge=True) == [0, 0, 1]
    assert msm.get(topology, element='system', formal_charge=True) == [0, 0, 1]


def test_instance_availability_distinguishes_capability_from_stored_values():
    topology = Topology(n_atoms=2)

    assert msm.has_attribute(topology, 'formal_charge', include_none=True)
    assert not msm.has_attribute(topology, 'formal_charge')
    assert msm.get(topology, element='atom', formal_charge=True) is None

    msm.set(topology, element='atom', formal_charge=[0, 1])

    assert msm.has_attribute(topology, 'formal_charge')


def test_mixed_get_combines_stable_and_chemical_state_attributes():
    topology = Topology(n_atoms=2)
    topology.atoms['atom_name'] = ['N', 'O']
    msm.set(topology, element='atom', formal_charge=[1, -1])

    assert msm.get(
        topology, element='atom', atom_name=True, formal_charge=True
    ) == [['N', 'O'], [1, -1]]


def test_chemical_state_selection_resolves_values_and_rejects_unavailable_data():
    topology = Topology(n_atoms=4)
    msm.set(
        topology,
        element='atom',
        formal_charge=[0, -1, 1, 0],
        atom_is_aromatic=[False, True, True, False],
    )

    assert msm.select(
        topology, selection='formal_charge!=0 and atom_is_aromatic==True'
    ) == [1, 2]

    empty = Topology(n_atoms=2)
    with pytest.raises(StructuralInconsistencyError, match='unavailable'):
        msm.select(empty, selection='formal_charge==0')


def test_chemical_state_access_fails_when_multiple_states_have_no_reference():
    topology = Topology(n_atoms=2)
    topology._append_chemical_state(state_id='product')
    topology._set_reference_chemical_state_index(None)

    with pytest.raises(StructuralInconsistencyError, match='ambiguous'):
        msm.get(topology, element='atom', formal_charge=True)
    with pytest.raises(StructuralInconsistencyError, match='ambiguous'):
        msm.select(topology, selection='formal_charge==0')


def test_molsys_formal_charge_writes_only_to_chemical_state():
    molsys = MolSys(n_atoms=3)
    molsys.molecular_mechanics.formal_charge = [1, 1, 1]

    msm.set(molsys, element='atom', formal_charge=[0, 1, -1])

    assert msm.get(molsys, element='atom', formal_charge=True) == [0, 1, -1]
    assert molsys.molecular_mechanics.formal_charge is None


def test_legacy_formal_charge_conflict_fails_closed():
    topology = Topology(n_atoms=2)
    topology._legacy_formal_charge = [0, 1]
    mechanics = MolecularMechanics()
    mechanics._legacy_formal_charge = [0, -1]
    restored = MolSys.__new__(MolSys)

    with pytest.raises(StructuralInconsistencyError, match='conflicting values'):
        restored.__setstate__(
            {
                'topology': topology,
                'structures': MolSys().structures,
                'molecular_mechanics': mechanics,
            }
        )
