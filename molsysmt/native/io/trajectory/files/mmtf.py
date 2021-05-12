def from_mmtf(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_mmtf import to_mmtf_MMTFDecoder as mmtf_to_mmtf_MMTFDecoder
    from molsysmt.native.io.trajectory.classes import from_mmtf_MMTFDecoder as mmtf_MMTFDecoder_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = mmtf_to_mmtf_MMTFDecoder(item, molecular_system)
    tmp_item, tmp_molecular_system = mmtf_MMTFDecoder_to_molsysmt_Trajectory(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

