from collections import namedtuple

Dependency = namedtuple('Dependency', ['name', 'type', 'pypi', 'conda'])

dependencies = {
    # Hard Dependencies
    'numpy': Dependency('numpy', 'hard', 'numpy', 'numpy'),
    'pandas': Dependency('pandas', 'hard', 'pandas', 'pandas'),
    'pyunitwizard': Dependency('pyunitwizard', 'hard', 'pyunitwizard', 'pyunitwizard'),
    'networkx': Dependency('networkx', 'hard', 'networkx', 'networkx'),
    'h5py': Dependency('h5py', 'hard', 'h5py', 'h5py'),
    'numba': Dependency('numba', 'hard', 'numba', 'numba'),
    'matplotlib': Dependency('matplotlib', 'hard', 'matplotlib', 'matplotlib'),
    'argdigest': Dependency('argdigest', 'hard', 'argdigest', 'argdigest'),
    'mmcif': Dependency('mmcif', 'hard', 'mmcif', 'mmcif'),

    # Soft Dependencies
    'mdtraj': Dependency('mdtraj', 'soft', 'mdtraj', 'mdtraj'),
    'MDAnalysis': Dependency('mdanalysis', 'soft', 'MDAnalysis', 'mdanalysis'),
    'openmm': Dependency('openmm', 'soft', 'openmm', 'openmm'),
    'openmmtools': Dependency('openmmtools', 'soft', 'openmmtools', 'openmmtools'),
    'parmed': Dependency('parmed', 'soft', 'parmed', 'parmed'),
    'pytraj': Dependency('pytraj', 'soft', 'pytraj', 'pytraj'),
    'nglview': Dependency('nglview', 'soft', 'nglview', 'nglview'),
    'pdbfixer': Dependency('pdbfixer', 'soft', 'pdbfixer', 'pdbfixer'),
    'biopython': Dependency('biopython', 'soft', 'biopython', 'biopython'),
    'plotly': Dependency('plotly', 'soft', 'plotly', 'plotly'),
    'mmtf': Dependency('mmtf', 'soft', 'mmtf-python', 'mmtf-python'),
}

# Mapping of form directory names to their required library key in the dependencies dict.
# This allows discovery without importing the modules.
form_dir_to_library = {
    # MDTraj based
    'mdtraj_Trajectory': 'mdtraj',
    'mdtraj_Topology': 'mdtraj',
    'mdtraj_DCDTrajectoryFile': 'mdtraj',
    'mdtraj_HDF5TrajectoryFile': 'mdtraj',
    'mdtraj_XTCTrajectoryFile': 'mdtraj',
    'file_xtc': 'mdtraj',
    'file_dcd': 'mdtraj',
    'file_h5': 'mdtraj',
    'file_mmtf': 'mdtraj',

    # OpenMM based
    'openmm_Topology': 'openmm',
    'openmm_System': 'openmm',
    'openmm_Context': 'openmm',
    'openmm_Simulation': 'openmm',
    'openmm_Modeller': 'openmm',
    'openmm_PDBFile': 'openmm',
    'openmm_AmberInpcrdFile': 'openmm',
    'openmm_AmberPrmtopFile': 'openmm',
    'openmm_CharmmCrdFile': 'openmm',
    'openmm_CharmmPsfFile': 'openmm',
    'openmm_GromacsGroFile': 'openmm',
    'openmm_GromacsTopFile': 'openmm',
    'openmm_State': 'openmm',
    'file_inpcrd': 'openmm',
    'file_prmtop': 'openmm',
    'file_psf': 'openmm',
    'file_gro': 'openmm',

    # MDAnalysis based
    'MDAnalysis_Universe': 'MDAnalysis',
    'MDAnalysis_Topology': 'MDAnalysis',

    # NGLView based
    'nglview_NGLWidget': 'nglview',

    # Parmed based
    'parmed_Structure': 'parmed',
    'file_mol2': 'parmed',

    # Pytraj based
    'pytraj_Trajectory': 'pytraj',
    'pytraj_Topology': 'pytraj',

    # Pdbfixer based
    'pdbfixer_PDBFixer': 'pdbfixer',

    # Biopython based
    'biopython_Seq': 'biopython',
    'biopython_SeqRecord': 'biopython',

    # MMTF based
    'mmtf_MMTFDecoder': 'mmtf',
}
