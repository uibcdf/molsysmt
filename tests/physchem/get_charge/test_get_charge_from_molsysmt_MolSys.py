"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
from openmm import app
import openmm as mm
from openmm import unit

def test_get_charge_from_molsysmt_MolSys_1():

    molsys = msm.systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(molsys, selection='molecule_type=="protein"')
    charge_residues = msm.physchem.get_charge(molsys, element='group', definition='physical_pH7')
    charge_residues = puw.get_value(charge_residues, to_unit='elementary_charge')
    charge_system = msm.physchem.get_charge(molsys, element='system', definition='physical_pH7')
    charge_system = puw.get_value(charge_system, to_unit='elementary_charge')

    good_charges_residues = np.array([ 0. ,  0. ,  0. ,  0. , -1. ,  0. ,  0. ,  1. ,  0. , -1. , -1. ,
                                       0. ,  0. ,  1. ,  0. ,  1. ,  0. ,  0. ,  1. , -1. ,  0. , -1. ,
                                       0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.1,  0. ,  0. ,
                                       0. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ,  0. ,
                                      -1. ,  0. , -1. ,  1. ,  0. ,  0. ,  0. ,  1. ,  0. ,  0. ,  0. ,
                                       0. ,  0. ,  0. ,  0. ,  1. , -1. , -1. ,  0. , -1. ,  1. ,  0. ,
                                       0. ,  0. ,  0. , -1. ,  0. , -1. ,  0. ,  0. ,  0. ,  1. ,  0. ,
                                       0. ,  0. ,  1. ,  0. ,  0. ,  1. ,  0. ,  1. ,  0. ,  0. ,  0. ,
                                      -1. ,  0. ,  0. , -1. ,  0. ,  0. ,  1. ,  1. ,  0. ,  0. ,  0. ,
                                       0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -1. ,  0. ,  0. ,
                                       0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ,  0. ,  0. ,
                                       0. ,  0. ,  1. ,  1. ,  0. , -1. , -1. ,  0. ,  0. ,  0. ,  0. ,
                                       0. ,  0. ,  1. ,  0. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,
                                       0. ,  1. ,  0. ,  1. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ,
                                       0. ,  0. ,  0. ,  0. , -1. ,  0. ,  0. ,  1. ])
    good_charge_system = 8.1

    assert np.allclose(charge_residues, good_charges_residues)
    assert np.allclose(charge_system, good_charge_system)


def test_get_charge_from_molsysmt_MolSys_2():

    molsys = msm.systems['Trp-Cage']['1l2y.h5msm']
    openmm_topology = msm.convert(molsys, to_form='openmm.Topology')

    charge_atoms = msm.physchem.get_charge(openmm_topology, element='atom', forcefield='AMBER14',
                                           definition='OpenMM')
    charge_groups = msm.physchem.get_charge(openmm_topology, element='group', forcefield='AMBER14',
                                            definition='OpenMM')
    charge_system = msm.physchem.get_charge(openmm_topology, element='system', forcefield='AMBER14',
                                            definition='OpenMM')
    
    n_atoms = msm.get(openmm_topology, n_atoms=True)

    charge_atoms = puw.get_value(charge_atoms, to_unit='elementary_charge')
    charge_groups = puw.get_value(charge_groups, to_unit='elementary_charge')
    charge_system = puw.get_value(charge_system, to_unit='elementary_charge')

    good_charge_atoms_1_10 = [0.1801, 0.0368, 0.6163, -0.5722, -0.0283, 0.5833, -0.5744, -0.8634, 0.1921, 0.1921]
    good_charge_groups = [1.0, -0.0, 0.0, -0.0, 0.0, 0.0, -0.0, 1.0, -1.0, 0.0, 0.0,
                          -0.0, 0.0, 0.0, 0.0, 1.0, -0.0, -0.0, -0.0, -1.0] 
    good_charge_system = 1.0

    assert np.allclose(charge_atoms[0:10], good_charge_atoms_1_10)
    assert np.allclose(charge_groups, good_charge_groups)
    assert np.allclose(charge_system, good_charge_system)


def test_get_charge_from_molsysmt_MolSys_3():

    molsys = msm.systems['Trp-Cage']['1l2y.h5msm']
    openmm_topology = msm.convert(molsys, to_form='openmm.Topology')
    forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    system = forcefield.createSystem(openmm_topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds)

    charge_atoms = msm.physchem.get_charge(system, element='atom', forcefield='AMBER14',
                                           definition='OpenMM')
    charge_system = msm.physchem.get_charge(system, element='system', forcefield='AMBER14',
                                            definition='OpenMM')
    
    n_atoms = msm.get(system, n_atoms=True)

    charge_atoms = puw.get_value(charge_atoms, to_unit='elementary_charge')
    charge_system = puw.get_value(charge_system, to_unit='elementary_charge')

    good_charge_atoms_1_10 = [0.1801, 0.0368, 0.6163, -0.5722, -0.0283, 0.5833, -0.5744, -0.8634, 0.1921, 0.1921]
    good_charge_system = 1.0

    assert np.allclose(charge_atoms[0:10], good_charge_atoms_1_10)
    assert np.allclose(charge_system, good_charge_system)


def test_get_charge_from_molsysmt_MolSys_4():

    molsys = msm.systems['Trp-Cage']['1l2y.h5msm']
    openmm_topology = msm.convert(molsys, to_form='openmm.Topology')
    forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    system = forcefield.createSystem(openmm_topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds)
    integrator = mm.LangevinIntegrator(300*unit.kelvin, 1.0/unit.picosecond, 2.0*unit.femtoseconds)
    platform = mm.Platform.getPlatformByName('CPU')
    simulation = app.Simulation(openmm_topology, system, integrator, platform)


    charge_atoms = msm.physchem.get_charge(simulation, element='atom', forcefield='AMBER14',
                                           definition='OpenMM')
    charge_groups = msm.physchem.get_charge(simulation, element='group', forcefield='AMBER14',
                                            definition='OpenMM')
    charge_system = msm.physchem.get_charge(simulation, element='system', forcefield='AMBER14',
                                            definition='OpenMM')
    
    n_atoms = msm.get(simulation, n_atoms=True)

    charge_atoms = puw.get_value(charge_atoms, to_unit='elementary_charge')
    charge_groups = puw.get_value(charge_groups, to_unit='elementary_charge')
    charge_system = puw.get_value(charge_system, to_unit='elementary_charge')

    good_charge_atoms_1_10 = [0.1801, 0.0368, 0.6163, -0.5722, -0.0283, 0.5833, -0.5744, -0.8634, 0.1921, 0.1921]
    good_charge_groups = [1.0, -0.0, 0.0, -0.0, 0.0, 0.0, -0.0, 1.0, -1.0, 0.0, 0.0,
                          -0.0, 0.0, 0.0, 0.0, 1.0, -0.0, -0.0, -0.0, -1.0] 
    good_charge_system = 1.0

    assert np.allclose(charge_atoms[0:10], good_charge_atoms_1_10)
    assert np.allclose(charge_groups, good_charge_groups)
    assert np.allclose(charge_system, good_charge_system)


