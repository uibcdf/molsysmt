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
}

# Mapping of form directory names to their required library key in the dependencies dict.
# This allows discovery without importing the modules.
form_dir_to_library = {
    'mdtraj_Trajectory': 'mdtraj',
    'mdtraj_Topology': 'mdtraj',
    'openmm_Topology': 'openmm',
    'openmm_System': 'openmm',
    'openmm_Context': 'openmm',
    'openmm_Simulation': 'openmm',
    'openmm_Modeller': 'openmm',
    'openmm_PDBFile': 'openmm',
    'MDAnalysis_Universe': 'MDAnalysis',
    'MDAnalysis_Topology': 'MDAnalysis',
    'nglview_NGLWidget': 'nglview',
    'parmed_Structure': 'parmed',
    'pytraj_Trajectory': 'pytraj',
    'pytraj_Topology': 'pytraj',
    'pdbfixer_PDBFixer': 'pdbfixer',
    'biopython_Seq': 'biopython',
    'biopython_SeqRecord': 'biopython',
}