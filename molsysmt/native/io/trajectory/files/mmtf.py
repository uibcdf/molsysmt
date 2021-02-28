def from_mmtf(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_mmtf import to_mmtf_MMTFDecoder as mmtf_to_mmtf_MMTFDecoder
    from molsysmt.native.io.trajectory.classes import from_mmtf_MMTFDecoder as mmtf_MMTFDecoder_to_molsysmt_Trajectory

    tmp_item = mmtf_to_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all')
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

