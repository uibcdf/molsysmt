"""Testing ParmEd chemistry and mechanics separation during conversion."""

import pytest
import numpy as np

import molsysmt as msm


def _chemical_structure():
    pmd = pytest.importorskip('parmed')
    from parmed.topologyobjects import QualitativeBondType

    structure = pmd.Structure()
    atoms = []
    for name, atomic_number, formal_charge, aromatic in (
        ('C1', 6, 0, True),
        ('C2', 6, 0, True),
        ('N', 7, 1, None),
        ('O', 8, -1, None),
    ):
        atom = pmd.Atom(
            name=name,
            type=name,
            atomic_number=atomic_number,
            formal_charge=formal_charge,
            aromatic=aromatic,
        )
        structure.add_atom(atom, 'LIG', 7, chain='A')
        atoms.append(atom)

    mechanical_type = pmd.BondType(100.0, 1.4)
    structure.bond_types.append(mechanical_type)
    structure.bond_types.claim()
    structure.bonds.append(
        pmd.Bond(
            atoms[0], atoms[1], type=mechanical_type, order=1.5,
            qualitative_type=QualitativeBondType.AROMATIC,
        )
    )
    structure.bonds.append(
        pmd.Bond(
            atoms[1], atoms[2], order=1,
            qualitative_type=QualitativeBondType.DATIVE,
        )
    )
    structure.bonds.append(
        pmd.Bond(
            atoms[2], atoms[3], order=1,
            qualitative_type=QualitativeBondType.HYDROGEN,
        )
    )
    return structure


def test_parmed_preserves_chemistry_without_promoting_force_parameters():
    topology = msm.convert(_chemical_structure(), to_form='molsysmt.Topology')

    assert msm.get(topology, element='atom', formal_charge=True) == [0, 0, 1, -1]
    assert msm.get(topology, element='atom', atom_is_aromatic=True)[:2] == [True, True]
    assert msm.get(topology, element='bond', fractional_bond_order=True)[0] == 1.5
    assert msm.get(topology, element='bond', bond_is_aromatic=True)[0] is True
    assert msm.get(topology, element='bond', bond_type=True) == ['covalent', 'dative']
    assert msm.get(topology, element='bond', bond_joins_components=True) == [True, False]
    assert msm.get(topology, element='system', n_bonds=True) == 2
    assert msm.get(topology, element='system', n_components=True) == 3


def test_parmed_reports_mechanics_and_nonbonded_relationship_loss():
    source = _chemical_structure()

    _, report = msm.convert(
        source,
        to_form='molsysmt.Topology',
        return_report=True,
    )

    assert report.outcome == 'lossy'
    assert {issue.attribute for issue in report.issues} == {
        'bond_type', 'bond_mechanical_parameters'
    }
    with pytest.raises(msm.NotCompatibleConversionError, match='Strict conversion'):
        msm.convert(source, to_form='molsysmt.Topology', strict=True)


def test_parmed_extracts_atoms_and_structures():
    source = _chemical_structure()
    source.coordinates = np.arange(24, dtype=float).reshape(2, 4, 3)

    extracted = msm.extract(source, selection=[0, 2], structure_indices=[1])

    assert len(extracted.atoms) == 2
    assert extracted.get_coordinates('all').shape == (1, 2, 3)


def test_parmed_converts_to_mdtraj_trajectory():
    pytest.importorskip('mdtraj')
    source = _chemical_structure()
    source.coordinates = np.arange(24, dtype=float).reshape(2, 4, 3)

    trajectory = msm.convert(source, to_form='mdtraj.Trajectory')

    assert trajectory.n_atoms == 4
    assert trajectory.n_frames == 2
