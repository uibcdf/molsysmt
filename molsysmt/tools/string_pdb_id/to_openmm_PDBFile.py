def to_openmm_PDBFile(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    if check_form:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check_form=check_form)

    from molsysmt.tools.string_pdb_id import to_molsysmt_MolSys as string_pdb_id_to_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_openmm_Modeller as molsysmt_MolSys_to_openmm_PDBFile

    tmp_item = string_pdb_id_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)
    tmp_item = molsysmt_MolSys_to_openmm_PDBFile(tmp_item, check_form=False)

    return tmp_item

