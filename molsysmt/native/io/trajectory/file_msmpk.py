def from_file_msmpk(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_file_msmpk import to_molsysmt_MolSys as file_msmpk_to_molsysmt_MolSys
    from molsysmt.api_forms.api_molsysmt_MolSys import to_molsysmt_Trajectory as molsysmt_MolSys_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = file_msmpk_to_molsysmt_MolSys(item,
            molecular_system=molecular_system, atom_indices=atom_indices,
            structure_indices=structure_indices)

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_molsysmt_Trajectory(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

