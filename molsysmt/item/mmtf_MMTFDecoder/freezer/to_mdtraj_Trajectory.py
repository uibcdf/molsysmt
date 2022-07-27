def to_mdtraj_Trajectory(item, selection='all', structure_indices='all', syntax='MolSysMT'):

    if check:
        from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import _checking_form
        _checking_form(item, check=check)

    from molsysmt.tools.mmtf_MMTFDecoder.to_molsysmt_MolSys import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys.to_mdtraj_Trajectory import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = molsysmt_MolSys_to_mdtraj_Trajectory(tmp_item)

    return tmp_item

