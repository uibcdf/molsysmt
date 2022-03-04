def to_openmm_Modeller(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    if check:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check=check)

    from molsysmt.tools.string_pdb_id import to_molsysmt_MolSys as string_pdb_id_to_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_openmm_Modeller as molsysmt_MolSys_to_openmm_Modeller

    tmp_item = string_pdb_id_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = molsysmt_MolSys_to_openmm_Modeller(tmp_item, check=False)

    return tmp_item

