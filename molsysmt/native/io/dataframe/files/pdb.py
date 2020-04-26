def from_pdb(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_pdb import to_openmm_PDBFile as pdb_to_openmm_PDBFile
    from molsysmt.native.io.dataframe.classes import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_DataFrame

    tmp_item = pdb_to_openmm_PDBFile(item)
    tmp_item = openmm_PDBFile_to_molsysmt_DataFrame(tmp_item)

    return tmp_item

