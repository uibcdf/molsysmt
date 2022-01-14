def from_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_file_pdb import to_openmm_PDBFile as file_pdb_to_openmm_PDBFile
    from molsysmt.native.io.topology import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = file_pdb_to_openmm_PDBFile(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_PDBFile_to_molsysmt_Topology(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

