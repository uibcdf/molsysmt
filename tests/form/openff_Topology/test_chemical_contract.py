"""Testing multi-molecule OpenFF topology chemistry boundaries."""

from importlib.util import find_spec

import numpy as np
import pytest

if find_spec('openff.toolkit') is None:
    pytest.skip('openff-toolkit is not installed', allow_module_level=True)

import openff.toolkit.topology as openff_topology
from openff.units import unit

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def _charged_topology():
    first = openff_topology.Molecule.from_smiles('CO')
    second = openff_topology.Molecule.from_smiles('O')
    first_charges = np.linspace(-0.3, 0.2, first.n_atoms)
    second_charges = np.linspace(-0.1, 0.1, second.n_atoms)
    first.partial_charges = first_charges * unit.elementary_charge
    second.partial_charges = second_charges * unit.elementary_charge
    topology = openff_topology.Topology.from_molecules([first, second])
    return topology, np.concatenate((first_charges, second_charges))


def test_openff_topology_keeps_local_duplicate_ids_and_global_indices():
    topology, _ = _charged_topology()

    native = msm.convert(topology, to_form='molsysmt.Topology')

    first_size = next(iter(topology.molecules)).n_atoms
    assert native.atoms['atom_id'].iloc[0] == '0'
    assert native.atoms['atom_id'].iloc[first_size] == '0'
    assert native.atoms.index.tolist() == list(range(topology.n_atoms))
    assert msm.get(native, element='system', n_components=True) == 2


def test_openff_topology_delivers_complete_partial_charges():
    topology, expected = _charged_topology()

    assert msm.has_attribute(topology, 'partial_charge')
    observed = msm.get(topology, element='atom', partial_charge=True)
    np.testing.assert_allclose(
        puw.get_value(observed, to_unit='elementary_charge'), expected
    )
    native = msm.convert(topology, to_form='molsysmt.MolSys')
    np.testing.assert_allclose(
        np.asarray(native.molecular_mechanics.partial_charge, dtype=float),
        expected,
    )


def test_openff_topology_does_not_invent_a_synchronized_trajectory():
    first = openff_topology.Molecule.from_smiles('CO')
    second = openff_topology.Molecule.from_smiles('O')
    first.add_conformer(
        np.zeros((first.n_atoms, 3), dtype=float) * unit.angstrom
    )
    second.add_conformer(
        np.ones((second.n_atoms, 3), dtype=float) * unit.angstrom
    )
    topology = openff_topology.Topology.from_molecules([first, second])

    assert not msm.has_attribute(topology, 'coordinates')
    structures = msm.convert(topology, to_form='molsysmt.Structures')
    assert structures.coordinates is None
