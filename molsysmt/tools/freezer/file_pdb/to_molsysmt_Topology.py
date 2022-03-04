def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all', check=True):

    if check:
        from molsysmt.tools.file_pdb.is_file_pdb import _checking_form
        _checking_form(item, check=check)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile as file_pdb_to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = file_pdb_to_openmm_PDBFile(item, molecular_system=molecular_system, check=False)
    tmp_item = openmm_PDBFile_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

