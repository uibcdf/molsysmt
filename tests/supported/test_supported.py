"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np


def test_supported_1():

    df = msm.supported.forms()
    df_data = list([ii,jj] for ii,jj in zip(df.data["Form"], df.data["Type"]))

    good_df_data = [['biopython.Seq', 'class'],
                    ['biopython.SeqRecord', 'class'],
                    ['MDAnalysis.Topology', 'class'],
                    ['MDAnalysis.Universe', 'class'],
                    ['mdtraj.DCDTrajectoryFile', 'class'],
                    ['mdtraj.HDF5TrajectoryFile', 'class'],
                    ['mdtraj.Topology', 'class'],
                    ['mdtraj.Trajectory', 'class'],
                    ['mdtraj.XTCTrajectoryFile', 'class'],
                    ['mmcif.PdbxContainers.DataContainer', 'class'],
                    ['mmtf.MMTFDecoder', 'class'],
                    ['molsysmt.CIFFileHandler', 'class'],
                    ['molsysmt.GROFileHandler', 'class'],
                    ['molsysmt.H5MSMFileHandler', 'class'],
                    ['molsysmt.MolecularMechanics', 'class'],
                    ['molsysmt.MolecularMechanicsDict', 'class'],
                    ['molsysmt.MolSys', 'class'],
                    ['molsysmt.PDBFileHandler', 'class'],
                    ['molsysmt.Structures', 'class'],
                    ['molsysmt.StructuresDict', 'class'],
                    ['molsysmt.Topology', 'class'],
                    ['networkx.Graph', 'class'],
                    ['nglview.NGLWidget', 'class'],
                    ['openmm.AmberInpcrdFile', 'class'],
                    ['openmm.AmberPrmtopFile', 'class'],
                    ['openmm.CharmmCrdFile', 'class'],
                    ['openmm.CharmmPsfFile', 'class'],
                    ['openmm.Context', 'class'],
                    ['openmm.GromacsGroFile', 'class'],
                    ['openmm.GromacsTopFile', 'class'],
                    ['openmm.Modeller', 'class'],
                    ['openmm.PDBFile', 'class'],
                    ['openmm.Simulation', 'class'],
                    ['openmm.State', 'class'],
                    ['openmm.System', 'class'],
                    ['openmm.Topology', 'class'],
                    ['parmed.Structure', 'class'],
                    ['pdbfixer.PDBFixer', 'class'],
                    ['pytraj.Topology', 'class'],
                    ['pytraj.Trajectory', 'class'],
                    ['XYZ', 'class'],
                    ['file:bcif', 'file'],
                    ['file:bcif.gz', 'file'],
                    ['file:cif', 'file'],
                    ['file:crd', 'file'],
                    ['file:dcd', 'file'],
                    ['file:gro', 'file'],
                    ['file:h5', 'file'],
                    ['file:h5msm', 'file'],
                    ['file:inpcrd', 'file'],
                    ['file:mmtf', 'file'],
                    ['file:mol2', 'file'],
                    ['file:msmpk', 'file'],
                    ['file:pdb', 'file'],
                    ['file:prmtop', 'file'],
                    ['file:psf', 'file'],
                    ['file:trjpk', 'file'],
                    ['file:xtc', 'file'],
                    ['file:xyznpy', 'file'],
                    ['string:alphafold_id', 'string'],
                    ['string:amino_acids_1', 'string'],
                    ['string:amino_acids_3', 'string'],
                    ['string:pdb_id', 'string'],
                    ['string:pdb_text', 'string']]


    all_good = True

    for ii,jj in zip(df_data, good_df_data):
        if not np.all(ii==jj):
            all_good = False
            break

    assert all_good


def test_supported_2():

    df = msm.supported.conversions()

    good_aux_list = ['biopython.Seq', 'biopython.SeqRecord', 'file:bcif', 'file:bcif.gz',
       'file:cif', 'file:crd', 'file:dcd', 'file:gro', 'file:h5', 'file:h5msm',
       'file:inpcrd', 'file:mmtf', 'file:mol2', 'file:msmpk', 'file:pdb',
       'file:prmtop', 'file:psf', 'file:trjpk', 'file:xtc', 'file:xyznpy',
       'MDAnalysis.Topology', 'MDAnalysis.Universe',
       'mdtraj.DCDTrajectoryFile', 'mdtraj.HDF5TrajectoryFile',
       'mdtraj.Topology', 'mdtraj.Trajectory', 'mdtraj.XTCTrajectoryFile',
       'mmcif.PdbxContainers.DataContainer', 'mmtf.MMTFDecoder',
       'molsysmt.CIFFileHandler', 'molsysmt.GROFileHandler',
       'molsysmt.H5MSMFileHandler', 'molsysmt.MolecularMechanics',
       'molsysmt.MolecularMechanicsDict', 'molsysmt.MolSys',
       'molsysmt.PDBFileHandler', 'molsysmt.Structures',
       'molsysmt.StructuresDict', 'molsysmt.Topology', 'networkx.Graph',
       'nglview.NGLWidget', 'openmm.AmberInpcrdFile', 'openmm.AmberPrmtopFile',
       'openmm.CharmmCrdFile', 'openmm.CharmmPsfFile', 'openmm.Context',
       'openmm.GromacsGroFile', 'openmm.GromacsTopFile', 'openmm.Modeller',
       'openmm.PDBFile', 'openmm.Simulation', 'openmm.State', 'openmm.System',
       'openmm.Topology', 'parmed.Structure', 'pdbfixer.PDBFixer',
       'pytraj.Topology', 'pytraj.Trajectory', 'string:alphafold_id',
       'string:amino_acids_1', 'string:amino_acids_3', 'string:pdb_id',
       'string:pdb_text', 'XYZ']

    assert list(df.index)==good_aux_list
    assert list(df.columns)==good_aux_list


def test_supported_3():

    df = msm.supported.viewers()

    good_aux_list = ['biopython.Seq', 'biopython.SeqRecord', 'file:bcif', 'file:bcif.gz',
       'file:cif', 'file:crd', 'file:dcd', 'file:gro', 'file:h5', 'file:h5msm',
       'file:inpcrd', 'file:mmtf', 'file:mol2', 'file:msmpk', 'file:pdb',
       'file:prmtop', 'file:psf', 'file:trjpk', 'file:xtc', 'file:xyznpy',
       'MDAnalysis.Topology', 'MDAnalysis.Universe',
       'mdtraj.DCDTrajectoryFile', 'mdtraj.HDF5TrajectoryFile',
       'mdtraj.Topology', 'mdtraj.Trajectory', 'mdtraj.XTCTrajectoryFile',
       'mmcif.PdbxContainers.DataContainer', 'mmtf.MMTFDecoder',
       'molsysmt.CIFFileHandler', 'molsysmt.GROFileHandler',
       'molsysmt.H5MSMFileHandler', 'molsysmt.MolecularMechanics',
       'molsysmt.MolecularMechanicsDict', 'molsysmt.MolSys',
       'molsysmt.PDBFileHandler', 'molsysmt.Structures',
       'molsysmt.StructuresDict', 'molsysmt.Topology', 'networkx.Graph',
       'nglview.NGLWidget', 'openmm.AmberInpcrdFile', 'openmm.AmberPrmtopFile',
       'openmm.CharmmCrdFile', 'openmm.CharmmPsfFile', 'openmm.Context',
       'openmm.GromacsGroFile', 'openmm.GromacsTopFile', 'openmm.Modeller',
       'openmm.PDBFile', 'openmm.Simulation', 'openmm.State', 'openmm.System',
       'openmm.Topology', 'parmed.Structure', 'pdbfixer.PDBFixer',
       'pytraj.Topology', 'pytraj.Trajectory', 'string:alphafold_id',
       'string:amino_acids_1', 'string:amino_acids_3', 'string:pdb_id',
       'string:pdb_text', 'XYZ']

    assert list(df.index)==good_aux_list
    assert list(df.columns)==['nglview.NGLWidget']


