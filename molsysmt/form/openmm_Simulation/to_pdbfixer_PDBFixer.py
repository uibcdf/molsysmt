from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.Simulation to pdbfixer.PDBFixer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    pdbfixer.PDBFixer
        Resulting object in pdbfixer.PDBFixer form.


    .. versionadded:: 1.0.0
    """

    from .to_file_pdb import to_file_pdb as openmm_Simulation_to_file_pdb
    from molsysmt._private.files_and_directories import temp_filename
    from molsysmt.form.file_pdb.to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer as file_pdb_to_pdbfixer_PDBFixer
    from os import remove

    tmp_file = temp_filename(extension='pdb')
    tmp_item = openmm_Simulation_to_file_pdb(item, output_filename=tmp_file,
            atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item = file_pdb_to_pdbfixer_PDBFixer(tmp_file, skip_digestion=True)
    remove(tmp_file)

    return tmp_item

