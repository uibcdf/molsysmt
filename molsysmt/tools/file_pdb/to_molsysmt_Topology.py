def to_molsysmt_Topology(item, atom_indices='all', model_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.file_pdb.is_file_pdb import _checking_form
        _checking_form(item, check_form=check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile as file_pdb_to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = file_pdb_to_openmm_PDBFile(item, molecular_system=molecular_system, check_form=False)
    tmp_item = openmm_PDBFile_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, model_indices=model_indices, check_form=False)

    return tmp_item

