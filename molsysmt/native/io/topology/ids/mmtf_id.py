def from_mmtf_id(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.ids.api_mmtf_id import to_mmtf_MMTFDecoder as mmtf_to_mmtf_MMTFDecoder
    from molsysmt.native.io.topology.classes import from_mmtf_MMTFDecoder as mmtf_Decoder_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = mmtf_to_mmtf_MMTFDecoder(item, molecular_system)
    tmp_item, tmp_molecular_system = mmtf_Decoder_to_molsysmt_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

