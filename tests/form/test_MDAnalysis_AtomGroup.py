import pytest
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_MDAnalysis_AtomGroup_conversion():
    # Load a system into MDAnalysis Universe via openmm (Tier 1 path)
    molsys_file = systems['pentalanine']['traj_pentalanine.h5']
    openmm_topology = msm.convert(molsys_file, to_form='openmm.Topology')
    
    import MDAnalysis as mda
    # We can create a Universe from an OpenMM topology
    universe = mda.Universe(openmm_topology)
    
    # Create an AtomGroup (selection of CA atoms)
    ag = universe.select_atoms("name CA")
    assert ag.n_atoms == 5
    
    # Check if MolSysMT recognizes it
    assert msm.get_form(ag) == 'MDAnalysis.AtomGroup'
    
    # Convert to native MolSys
    molsys = msm.convert(ag, to_form='molsysmt.MolSys')
    assert msm.get(molsys, element='system', n_atoms=True) == 5
    
    # Check atom name parity
    names_ag = msm.get(ag, element='atom', name=True)
    names_msm = msm.get(molsys, element='atom', name=True)
    assert names_ag == names_msm
    assert all(n == 'CA' for n in names_msm)

def test_MDAnalysis_AtomGroup_get_coordinates():
    molsys_file = systems['pentalanine']['traj_pentalanine.h5']
    mdtraj_traj = msm.convert(molsys_file, to_form='mdtraj.Trajectory')
    
    import MDAnalysis as mda
    universe = mda.Universe(mdtraj_traj.topology.to_openmm(), mdtraj_traj.xyz * 10.0) # MDAnalysis needs Angstroms
    ag = universe.select_atoms("resname ALA") # All atoms of ALA residues
    
    coords = msm.get(ag, element='atom', coordinates=True)
    assert coords.shape[1] == ag.n_atoms
    assert str(msm.pyunitwizard.get_unit(coords)) == 'nanometer'
