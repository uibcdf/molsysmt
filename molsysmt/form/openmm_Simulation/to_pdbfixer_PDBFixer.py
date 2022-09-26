from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all'):

    from . import to_file_pdb as openmm_Simulation_to_file_pdb
    from molsysmt._private.files_and_directories import temp_filename
    from molsysmt.form.file_pdb import to_pdbfixer_PDBFixer as file_pdb_to_pdbfixer_PDBFixer
    from os import remove

    tmp_file = temp_filename(extension='pdb')
    tmp_item = molsysmt_Simulation_to_file_pdb(item, output_filename=tmp_file,
            atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = file_pdb_to_pdbfixer_PDBFixer(tmp_file)
    remove(tmp_pdbfile)

    return tmp_item

