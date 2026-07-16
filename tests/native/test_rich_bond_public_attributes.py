"""Testing public normalized chemical-state bond attributes."""

import pandas as pd

import molsysmt as msm
from molsysmt.native import MolSys, Topology


RICH_BOND_ATTRIBUTES = {
    'bond_id': ['shared', 'shared'],
    'bond_order': [1, 0],
    'fractional_bond_order': [1.0, 1.5],
    'bond_type': ['covalent', 'dative'],
    'bond_is_aromatic': [False, True],
    'bond_is_conjugated': [False, True],
    'bond_stereo_atom_indices': [[0, 1], [2, 3]],
    'bond_stereochemistry': ['unspecified', 'E'],
    'bond_donor_atom_index': [pd.NA, 2],
    'bond_acceptor_atom_index': [pd.NA, 3],
    'bond_joins_components': [True, False],
    'bond_evidence': ['explicit', 'explicit'],
}


def _rich_topology(container=Topology):
    item = container(n_atoms=4)
    topology = item.topology if isinstance(item, MolSys) else item
    topology._append_chemical_state_bonds([[0, 1], [2, 3]])
    for attribute in (
        'bond_evidence',
        'bond_stereo_atom_indices',
        'bond_id',
        'bond_order',
        'fractional_bond_order',
        'bond_type',
        'bond_is_aromatic',
        'bond_is_conjugated',
        'bond_stereochemistry',
        'bond_donor_atom_index',
        'bond_acceptor_atom_index',
        'bond_joins_components',
    ):
        msm.set(
            item,
            element='bond',
            **{attribute: RICH_BOND_ATTRIBUTES[attribute]},
        )
    return item


def test_topology_get_set_and_capability_deliver_every_rich_bond_attribute():
    topology = _rich_topology()

    observed = msm.get(
        topology,
        element='bond',
        output_type='dictionary',
        **{attribute: True for attribute in RICH_BOND_ATTRIBUTES},
    )

    for attribute, expected in RICH_BOND_ATTRIBUTES.items():
        assert observed[attribute] == expected
        assert msm.has_attribute(topology, attribute)
    assert msm.get(
        topology, element='bond', selection=[1], bond_is_aromatic=True
    ) == [True]
    assert msm.select(
        topology, 'bond_is_aromatic==True', element='bond'
    ) == [1]


def test_molsys_delegates_rich_bond_delivery_and_explicit_state_selection():
    molsys = _rich_topology(MolSys)
    product = molsys.topology._append_chemical_state(state_id='product')
    molsys.topology._append_chemical_state_bonds(
        [[0, 1]], orders=[2], state_index=product
    )

    assert msm.get(
        molsys, element='bond', chemical_state=0, bond_order=True
    ) == [1, 0]
    assert msm.get(
        molsys, element='bond', chemical_state=1, bond_order=True
    ) == [2]
    msm.set(
        molsys,
        element='bond',
        chemical_state=1,
        bond_evidence='user_defined',
    )
    assert msm.get(
        molsys, element='bond', chemical_state=1, bond_evidence=True
    ) == ['user_defined']


def test_optional_bond_capability_distinguishes_support_from_instance_values():
    topology = Topology(n_atoms=2)
    topology._append_chemical_state_bonds([[0, 1]])

    assert not msm.has_attribute(topology, 'fractional_bond_order')
    assert msm.has_attribute(
        topology, 'fractional_bond_order', include_none=True
    )
    assert msm.get(
        topology, element='bond', fractional_bond_order=True
    ) == [None]


def test_h5msm_v04_delivers_public_rich_bond_attributes(tmp_path):
    topology = _rich_topology()
    filename = tmp_path / 'rich_bonds.h5msm'

    msm.convert(topology, to_form=str(filename))

    assert msm.get(
        str(filename), element='bond', bond_id=True
    ) == ['shared', 'shared']
    assert msm.get(
        str(filename), element='bond', bond_is_aromatic=True
    ) == [False, True]
    assert msm.get(
        str(filename), element='bond', bond_stereo_atom_indices=True
    ) == [[0, 1], [2, 3]]
    assert msm.has_attribute(str(filename), 'bond_evidence')


def test_isotope_is_public_nullable_stable_topology_metadata():
    topology = Topology(n_atoms=3)

    msm.set(topology, element='atom', isotope=[13, None, 2])

    observed = msm.get(topology, element='atom', isotope=True)
    assert observed[0] == 13
    assert pd.isna(observed[1])
    assert observed[2] == 2
    assert str(topology.atoms['isotope'].dtype) == 'UInt16'
    assert msm.has_attribute(topology, 'isotope')
    assert msm.has_attribute(Topology(n_atoms=1), 'isotope', include_none=True)


def test_isotope_survives_native_dict_and_merge_paths():
    left = Topology(n_atoms=2)
    right = Topology(n_atoms=1)
    msm.set(left, element='atom', isotope=[13, None])
    msm.set(right, element='atom', isotope=2)

    payload = msm.convert(left, to_form='molsysmt.TopologyDict')
    restored = msm.convert(payload, to_form='molsysmt.Topology')
    merged = msm.merge([restored, right], to_form='molsysmt.Topology')

    observed = msm.get(merged, element='atom', isotope=True)
    assert observed[0] == 13
    assert pd.isna(observed[1])
    assert observed[2] == 2
