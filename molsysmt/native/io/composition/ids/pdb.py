def from_pdb(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.ids.api_pdb import to_openmm_PDBFile as pdb_to_openmm_PDBFile
    from molsysmt.native.io.composition.classes import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_Composition

    tmp_item = pdb_to_openmm_PDBFile(item, atom_indices='all', frame_indices='all')
    tmp_item = openmm_PDBFile_to_molsysmt_Composition(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

