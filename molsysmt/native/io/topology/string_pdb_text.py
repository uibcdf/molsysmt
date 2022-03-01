def from_string_pdb_text(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_string_pdb_text import to_openmm_PDBFile as string_pdb_text_to_openmm_PDBFile
    from molsysmt.native.io.topology import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = string_pdb_text_to_openmm_PDBFile(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_PDBFile_to_molsysmt_Topology(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

