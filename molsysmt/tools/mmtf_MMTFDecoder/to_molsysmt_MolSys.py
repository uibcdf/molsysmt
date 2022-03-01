def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import _checking_form
        _checking_form(item, check_form=check_form)

    from molsysmt.native.molsys import MolSys
    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology as mmtf_MMTFDecoder_to_molsysmt_Topology
    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Trajectory as mmtf_MMTFDecoder_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology = mmtf_MMTFDecoder_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)
    tmp_item.trajectory = mmtf_MMTFDecoder_to_molsysmt_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

