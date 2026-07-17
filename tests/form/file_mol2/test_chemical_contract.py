"""Testing Tripos MOL2 fidelity and explicit rejection boundaries."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import FormatError


CAFFEINE = msm.systems['caffeine']['caffeine.mol2']


def test_mol2_preserves_tripos_types_ids_charges_coordinates_and_amide_orders():
    native = msm.convert(CAFFEINE, to_form='molsysmt.MolSys')

    assert native.topology.atoms['atom_id'].iloc[:3].tolist() == ['1', '2', '3']
    assert native.topology.atoms['atom_type'].iloc[:3].tolist() == [
        'C.3', 'N.pl3', 'C.2'
    ]
    assert native.topology.bonds['bond_id'].iloc[:3].tolist() == ['1', '2', '3']
    amide_orders = native.topology.bonds['fractional_bond_order'].dropna()
    assert amide_orders.tolist() == pytest.approx([1.25, 1.25, 1.25])
    assert native.structures.coordinates.shape == (1, 24, 3)
    np.testing.assert_allclose(
        puw.get_value(
            native.structures.coordinates[0, 0], to_unit='angstrom'
        ),
        [-0.0178, 1.4608, 0.0101],
    )
    np.testing.assert_allclose(
        np.asarray(native.molecular_mechanics.partial_charge, dtype=float)[:3],
        [0.0684, -0.4126, 0.2683],
    )


def test_mol2_public_get_delivers_partial_charges_and_selection():
    charges = msm.get(CAFFEINE, element='atom', partial_charge=True)
    np.testing.assert_allclose(
        puw.get_value(charges, to_unit='elementary_charge')[:3],
        [0.0684, -0.4126, 0.2683],
    )

    subset = msm.convert(
        CAFFEINE, to_form='molsysmt.MolSys', selection=[1, 0]
    )
    assert subset.topology.atoms['atom_id'].tolist() == ['1', '2']
    assert subset.structures.coordinates.shape == (1, 2, 3)
    np.testing.assert_allclose(
        np.asarray(subset.molecular_mechanics.partial_charge, dtype=float),
        [0.0684, -0.4126],
    )


def test_mol2_aromatic_token_is_not_collapsed_to_an_integral_order(tmp_path):
    path = tmp_path / 'benzene.mol2'
    atoms = '\n'.join(
        f'{index} C{index} {index}.0 0.0 0.0 C.ar 1 BEN 0.0'
        for index in range(1, 7)
    )
    bonds = '\n'.join(
        f'{index} {index} {index + 1 if index < 6 else 1} ar'
        for index in range(1, 7)
    )
    path.write_text(
        '@<TRIPOS>MOLECULE\nBENZENE\n6 6 1 0 0\nSMALL\nNO_CHARGES\n\n'
        f'@<TRIPOS>ATOM\n{atoms}\n@<TRIPOS>BOND\n{bonds}\n',
        encoding='utf-8',
    )

    topology = msm.convert(str(path), to_form='molsysmt.Topology')

    assert all(topology.bonds['is_aromatic'])
    assert all(topology.bonds['fractional_bond_order'] == 1.5)
    assert 'bond_order' not in topology.bonds.columns
    assert not msm.has_attribute(str(path), 'partial_charge')


def test_mol2_rejects_multiple_molecule_records(tmp_path):
    record = (
        '@<TRIPOS>MOLECULE\nONE\n1 0 0 0 0\nSMALL\nNO_CHARGES\n\n'
        '@<TRIPOS>ATOM\n1 C1 0 0 0 C.3 1 MOL 0\n'
    )
    path = tmp_path / 'multiple.mol2'
    path.write_text(record + record, encoding='utf-8')

    with pytest.raises(FormatError, match='exactly one'):
        msm.convert(str(path), to_form='molsysmt.MolSys')


def test_mol2_rejects_unsupported_bond_tokens(tmp_path):
    path = tmp_path / 'unsupported.mol2'
    path.write_text(
        '@<TRIPOS>MOLECULE\nUNKNOWN\n2 1 0 0 0\nSMALL\nNO_CHARGES\n\n'
        '@<TRIPOS>ATOM\n'
        '1 C1 0 0 0 C.3 1 MOL 0\n'
        '2 C2 1 0 0 C.3 1 MOL 0\n'
        '@<TRIPOS>BOND\n1 1 2 du\n',
        encoding='utf-8',
    )

    with pytest.raises(FormatError):
        msm.convert(str(path), to_form='molsysmt.MolSys')
