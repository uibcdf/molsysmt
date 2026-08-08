"""The extra keywords `convert` forwards to the converter it resolves.

`msm.convert(molsys, to_form=...)` hands anything it does not recognise to the converter,
so what is admissible depends on the target form. This table says which keywords each
target accepts.

**Generated. Do not edit by hand.** Rewrite it with

    python devtools/scripts/generate_converter_arguments.py --write

and review the diff. `tests/test_argument_contract.py` fails if the file stops matching
the converters it was derived from, so a signature change shows up as a failing test with
a diff to apply, never as a silently wrong contract.

**Keyed by the target form only, deliberately.** The exact set depends on the pair
`(from_form, to_form)` -- for `file:pdb` alone there are six different sets depending on
where the conversion starts. But `from_form` is not an argument: deriving it from the
molecular system costs a significant fraction of the conversion itself, on every call.
Keying on the target admits the union across origins: 4.9 names on average where the exact
set averages 3.3. The comparison that matters is not 4.9 against 3.3, it is 4.9 against
*anything at all*. A mistyped keyword belongs to no union and is refused either way; what
gets through is a keyword valid for a different origin form, which the converter itself
rejects a moment later, where the origin is known.
"""

from argdigest import Domain

#: to_form -> the keywords some converter into that form accepts.
CONVERTER_ARGUMENTS = {
    'MDAnalysis.AtomGroup': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'MDAnalysis.Topology': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'MDAnalysis.Universe': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'MDAnalysis.topology.PDBParser': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'XYZ': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'biopython.PDBStructure': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'biopython.Seq': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'group_indices', 'int_precision', 'skip_digestion',
        'structure_indices'
    ),
    'biopython.SeqRecord': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'description',
        'float_precision', 'get_missing_bonds', 'group_indices', 'id', 'int_precision',
        'name', 'skip_digestion', 'structure_indices'
    ),
    'cupy_ndarray': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'file:bcif': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'output_name',
        'skip_digestion', 'structure_indices'
    ),
    'file:bcif.gz': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'output_name',
        'skip_digestion', 'structure_indices'
    ),
    'file:cif': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'output_name',
        'skip_digestion', 'structure_indices'
    ),
    'file:cif.gz': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'output_name',
        'skip_digestion', 'structure_indices'
    ),
    'file:crd': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_name', 'skip_digestion',
        'structure_indices'
    ),
    'file:dcd': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_name', 'skip_digestion',
        'structure_indices'
    ),
    'file:fasta': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'description',
        'float_precision', 'get_missing_bonds', 'id', 'int_precision', 'name',
        'output_filename', 'skip_digestion'
    ),
    'file:gro': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'skip_digestion',
        'structure_indices'
    ),
    'file:h5': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_name', 'skip_digestion',
        'structure_indices'
    ),
    'file:h5msm': (
        'atom_indices', 'compression', 'compression_opts', 'coordinates', 'copy_if_all',
        'float_precision', 'get_missing_bonds', 'int_precision', 'output_filename',
        'output_name', 'skip_digestion', 'structure_indices'
    ),
    'file:inpcrd': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_name', 'skip_digestion',
        'structure_indices'
    ),
    'file:mdcrd': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'skip_digestion',
        'structure_indices'
    ),
    'file:mol2': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'output_name',
        'skip_digestion', 'structure_indices'
    ),
    'file:molsys_yaml': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'skip_digestion',
        'structure_indices'
    ),
    'file:pdb': (
        'atom_indices', 'box', 'compression', 'compression_opts', 'coordinates',
        'copy_if_all', 'float_precision', 'get_missing_bonds', 'int_precision',
        'multiframe', 'output_filename', 'output_name', 'skip_digestion',
        'structure_indices'
    ),
    'file:pir': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'description',
        'float_precision', 'get_missing_bonds', 'id', 'int_precision', 'name',
        'output_filename', 'skip_digestion'
    ),
    'file:prmtop': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_name', 'skip_digestion',
        'structure_indices'
    ),
    'file:psf': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'skip_digestion',
        'structure_indices'
    ),
    'file:smi': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'name', 'output_filename', 'skip_digestion'
    ),
    'file:structures_yaml': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'skip_digestion',
        'structure_indices'
    ),
    'file:top': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'skip_digestion',
        'structure_indices'
    ),
    'file:topology_yaml': (
        'compression', 'compression_opts', 'float_precision', 'get_missing_bonds',
        'int_precision', 'output_filename', 'skip_digestion'
    ),
    'file:trjpk': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'output_name',
        'skip_digestion', 'structure_indices'
    ),
    'file:xtc': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'output_name',
        'skip_digestion', 'structure_indices'
    ),
    'file:xyz': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'skip_digestion',
        'structure_indices'
    ),
    'file:xyznpy': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'output_filename', 'output_name',
        'skip_digestion', 'structure_indices'
    ),
    'mdtraj.AmberRestartFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'mdtraj.DCDTrajectoryFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'mdtraj.GroTrajectoryFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'mdtraj.HDF5TrajectoryFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'mdtraj.PDBTrajectoryFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'mdtraj.Topology': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices',
        'syntax'
    ),
    'mdtraj.Trajectory': (
        'atom_indices', 'box', 'compression', 'compression_opts', 'coordinates',
        'copy_if_all', 'float_precision', 'get_missing_bonds', 'int_precision',
        'output_filename', 'skip_digestion', 'structure_indices'
    ),
    'mdtraj.XTCTrajectoryFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'mmcif.PdbxContainers.DataContainer': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.CIFFileHandler': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.GROFileHandler': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.H5MSMFileHandler': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.MolSys': (
        'atom_indices', 'box', 'compression', 'compression_opts', 'coordinates',
        'copy_if_all', 'float_precision', 'get_missing_bonds', 'int_precision',
        'skip_digestion', 'structure_id', 'structure_indices', 'time'
    ),
    'molsysmt.MolSysBuilder': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.MolSysDict': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.MolecularMechanics': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.MolecularMechanicsDict': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion'
    ),
    'molsysmt.PDBFileHandler': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.Structures': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.StructuresDict': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.Topology': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'molsysmt.TopologyDict': (
        'compression', 'compression_opts', 'float_precision', 'get_missing_bonds',
        'int_precision', 'skip_digestion'
    ),
    'molsysmt.ViewerJSON': (
        'compression', 'compression_opts', 'float_precision', 'get_missing_bonds',
        'int_precision', 'skip_digestion'
    ),
    'molsysviewer.MolSysView': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'networkx.Graph': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'nglview.NGLWidget': (
        'atom_indices', 'box', 'compression', 'compression_opts', 'coordinates',
        'copy_if_all', 'float_precision', 'get_missing_bonds', 'int_precision',
        'skip_digestion', 'structure_indices'
    ),
    'openff.Molecule': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'openff.Topology': (
        'compression', 'compression_opts', 'float_precision', 'get_missing_bonds',
        'int_precision', 'skip_digestion'
    ),
    'openmm.AmberInpcrdFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'openmm.AmberPrmtopFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'openmm.CharmmCrdFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'openmm.CharmmPsfFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'openmm.Context': (
        'atom_indices', 'compression', 'compression_opts', 'constraints', 'coordinates',
        'copy_if_all', 'dispersion_correction', 'ewald_error_tolerance', 'float_precision',
        'forcefield', 'friction', 'get_missing_bonds', 'implicit_solvent', 'int_precision',
        'integrator', 'non_bonded_method', 'platform', 'skip_digestion',
        'structure_indices', 'switch_distance', 'temperature', 'time_step', 'water_model'
    ),
    'openmm.GromacsGroFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'openmm.GromacsTopFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'openmm.Modeller': (
        'atom_indices', 'box', 'compression', 'compression_opts', 'coordinates',
        'copy_if_all', 'float_precision', 'get_missing_bonds', 'int_precision',
        'skip_digestion', 'structure_indices'
    ),
    'openmm.PDBFile': (
        'atom_indices', 'compression', 'compression_opts', 'coordinates', 'copy_if_all',
        'float_precision', 'get_missing_bonds', 'int_precision', 'skip_digestion',
        'structure_indices'
    ),
    'openmm.Simulation': (
        'atom_indices', 'collisions_rate', 'compression', 'compression_opts', 'constraints',
        'coordinates', 'copy_if_all', 'flexible_constraints', 'float_precision',
        'forcefield', 'get_missing_bonds', 'hydrogen_mass', 'int_precision',
        'integration_timestep', 'integrator', 'non_bonded_cutoff', 'non_bonded_method',
        'platform', 'remove_cm_motion', 'rigid_water', 'skip_digestion',
        'structure_indices', 'switch_distance', 'temperature'
    ),
    'openmm.State': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'openmm.System': (
        'atom_indices', 'compression', 'compression_opts', 'constraints', 'copy_if_all',
        'dispersion_correction', 'ewald_error_tolerance', 'flexible_constraints',
        'float_precision', 'forcefield', 'get_missing_bonds', 'hydrogen_mass',
        'implicit_solvent', 'int_precision', 'non_bonded_cutoff', 'non_bonded_method',
        'remove_cm_motion', 'rigid_water', 'skip_digestion', 'structure_indices',
        'switch_distance', 'water_model'
    ),
    'openmm.Topology': (
        'atom_indices', 'box', 'compression', 'compression_opts', 'copy_if_all',
        'float_precision', 'get_missing_bonds', 'int_precision', 'skip_digestion',
        'structure_indices'
    ),
    'parmed.GromacsTopologyFile': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'parmed.Structure': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'pdbfixer.PDBFixer': (
        'atom_indices', 'compression', 'compression_opts', 'coordinates', 'copy_if_all',
        'float_precision', 'get_missing_bonds', 'int_precision', 'pdb_chain_id',
        'skip_digestion', 'structure_indices'
    ),
    'pytraj.Topology': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'max_bond_length', 'skip_digestion',
        'structure_indices'
    ),
    'pytraj.Trajectory': (
        'atom_indices', 'box', 'compression', 'compression_opts', 'coordinates',
        'copy_if_all', 'float_precision', 'get_missing_bonds', 'int_precision',
        'skip_digestion', 'structure_indices'
    ),
    'rdkit.Mol': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'string:alphafold_id': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'string:amino_acids_1': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'group_indices', 'int_precision', 'output_filename',
        'skip_digestion', 'structure_indices'
    ),
    'string:amino_acids_3': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'group_indices', 'int_precision', 'skip_digestion'
    ),
    'string:pdb_id': (
        'atom_indices', 'compression', 'compression_opts', 'copy_if_all', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion', 'structure_indices'
    ),
    'string:pdb_text': (
        'atom_indices', 'box', 'compression', 'compression_opts', 'coordinates',
        'copy_if_all', 'float_precision', 'get_missing_bonds', 'int_precision',
        'pdb_chain_id', 'skip_digestion', 'structure_indices'
    ),
    'string:smiles': (
        'compression', 'compression_opts', 'float_precision', 'get_missing_bonds',
        'int_precision', 'skip_digestion'
    ),
    'string:uniprot_id': (
        'atom_indices', 'compression', 'compression_opts', 'float_precision',
        'get_missing_bonds', 'int_precision', 'skip_digestion'
    ),
}


domain = Domain(
    name='converter_arguments',
    depends_on='to_form',
    by_value=CONVERTER_ARGUMENTS,
    description='keywords the converters into a given target form accept',
)
