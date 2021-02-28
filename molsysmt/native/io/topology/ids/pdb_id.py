def from_pdb_id(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.ids.api_pdb import to_openmm_PDBFile as pdb_to_openmm_PDBFile
    from molsysmt.native.io.topology.classes import from_openmm_DataFile as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = pdb_to_openmm_PDBFile(item, atom_indices='all', frame_indices='all')
    tmp_item = openmm_PDBFile_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

