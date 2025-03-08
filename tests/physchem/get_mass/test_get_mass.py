"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
from openmm import app

# Distance between atoms in space and time

def test_get_mass_1():

    molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])

    mass_atoms = msm.physchem.get_mass(molsys, element='atom', selection='molecule_type=="protein"')
    mass_groups = msm.physchem.get_mass(molsys, element='group', selection='molecule_type=="protein"')
    mass_system = msm.physchem.get_mass(molsys, element='system')

    n_atoms = msm.get(molsys, selection='molecule_type=="protein"', n_atoms=True)
    n_groups = msm.get(molsys, selection='molecule_type=="protein"', n_groups=True)

    good_mass_atoms_1_10 = msm.pyunitwizard.quantity([14.007, 12.011, 12.011, 15.999, 12.011, 12.011, 32.06,
                                                      12.011, 14.007, 12.011], unit='dalton')
    good_mass_groups_1_10 = msm.pyunitwizard.quantity([122.121, 108.056, 102.072, 138.105, 122.059, 122.121,
                                                       102.072, 144.093, 102.072, 110.048], unit='dalton')

    assert len(mass_atoms)==n_atoms
    assert puw.are_close(mass_atoms[0:10], good_mass_atoms_1_10)
    assert len(mass_groups)==n_groups
    assert puw.are_close(mass_groups[0:10], good_mass_groups_1_10)
    assert puw.are_close(mass_system, puw.quantity(19463.62, 'dalton'))


def test_get_mass_2():

    molsys = msm.systems['Trp-Cage']['1l2y.h5msm']
    openmm_topology = msm.convert(molsys, to_form='openmm.Topology')

    mass_atoms = msm.physchem.get_mass(openmm_topology, element='atom', method='OpenMM')
    mass_groups = msm.physchem.get_mass(openmm_topology, element='group', method='OpenMM')
    mass_system = msm.physchem.get_mass(openmm_topology, element='system', method='OpenMM')

    n_atoms = msm.get(molsys, n_atoms=True)
    n_groups = msm.get(molsys, n_groups=True)

    good_mass_atoms_1_10 = msm.pyunitwizard.quantity([14.00672, 12.01078, 12.01078, 15.99943, 12.01078, 12.01078,
                                                      15.99943, 14.00672, 1.007947, 1.007947], unit='dalton')
    good_mass_groups_1_10 = msm.pyunitwizard.quantity([116.119, 113.158, 163.174, 113.158, 128.129, 186.211,
                                                       113.158, 129.181, 114.080, 57.051], unit='dalton')

    assert len(mass_atoms)==n_atoms
    assert puw.are_close(mass_atoms[0:10], good_mass_atoms_1_10)
    assert len(mass_groups)==n_groups
    assert puw.are_close(mass_groups[0:10], good_mass_groups_1_10)
    assert puw.are_close(mass_system, puw.quantity(2170.4134, 'dalton'))


def test_get_mass_3():

    molsys = msm.systems['Trp-Cage']['1l2y.h5msm']
    openmm_topology = msm.convert(molsys, to_form='openmm.Topology')

    forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    system = forcefield.createSystem(openmm_topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds)

    mass_atoms = msm.physchem.get_mass(system, element='atom', method='OpenMM')
    mass_system = msm.physchem.get_mass(system, element='system', method='OpenMM')

    n_atoms = msm.get(molsys, n_atoms=True)

    good_mass_atoms_1_10 = msm.pyunitwizard.quantity([14.01, 12.01, 12.01, 16.0, 12.01, 12.01,
                                                      16.0, 14.01, 1.008, 1.008], unit='dalton')

    assert len(mass_atoms)==n_atoms
    assert puw.are_close(mass_atoms[0:10], good_mass_atoms_1_10)
    assert puw.are_close(mass_system, puw.quantity(2170.45, 'dalton'))


