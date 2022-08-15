def from_pdb(item, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.ids.api_pdb import to_openmm_PDBFile as pdb_to_openmm_PDBFile
    from molsysmt.native.io.topology import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = pdb_to_openmm_PDBFile(item, atom_indices='all', structure_indices='all')
    tmp_item = openmm_PDBFile_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

