# DepDigest configuration for MolSysMT
from molsysmt._private.exceptions import LibraryNotFoundError

LIBRARIES = {
    'numpy': {'type': 'hard', 'pypi': 'numpy'},
    'pandas': {'type': 'hard', 'pypi': 'pandas'},
    'mdtraj': {'type': 'soft', 'pypi': 'mdtraj'},
    'openmm': {'type': 'soft', 'pypi': 'openmm'},
    'MDAnalysis': {'type': 'soft', 'pypi': 'MDAnalysis'},
    'parmed': {'type': 'soft', 'pypi': 'parmed'},
    'pytraj': {'type': 'soft', 'pypi': 'pytraj'},
    'nglview': {'type': 'soft', 'pypi': 'nglview'},
    'pdbfixer': {'type': 'soft', 'pypi': 'pdbfixer'},
    'biopython': {'type': 'soft', 'pypi': 'biopython'},
    'plotly': {'type': 'soft', 'pypi': 'plotly'},
    'mmtf': {'type': 'soft', 'pypi': 'mmtf-python'},
}

MAPPING = {
    'mdtraj_Trajectory': 'mdtraj',
    'mdtraj_Topology': 'mdtraj',
    'mdtraj_DCDTrajectoryFile': 'mdtraj',
    'mdtraj_HDF5TrajectoryFile': 'mdtraj',
    'mdtraj_XTCTrajectoryFile': 'mdtraj',
    'file_xtc': 'mdtraj',
    'file_dcd': 'mdtraj',
    'file_h5': 'mdtraj',
    'file_mmtf': 'mdtraj',
    'openmm_Topology': 'openmm',
    'openmm_System': 'openmm',
    'openmm_Context': 'openmm',
    'openmm_Simulation': 'openmm',
    'openmm_Modeller': 'openmm',
    'openmm_PDBFile': 'openmm',
    'file_inpcrd': 'openmm',
    'file_prmtop': 'openmm',
    'file_psf': 'openmm',
    'file_gro': 'openmm',
    'MDAnalysis_Universe': 'MDAnalysis',
    'MDAnalysis_Topology': 'MDAnalysis',
    'nglview_NGLWidget': 'nglview',
    'parmed_Structure': 'parmed',
    'file_mol2': 'parmed',
    'pytraj_Trajectory': 'pytraj',
    'pytraj_Topology': 'pytraj',
    'pdbfixer_PDBFixer': 'pdbfixer',
    'biopython_Seq': 'biopython',
    'biopython_SeqRecord': 'biopython',
    'mmtf_MMTFDecoder': 'mmtf',
}

SHOW_ALL_CAPABILITIES = True
EXCEPTION_CLASS = LibraryNotFoundError