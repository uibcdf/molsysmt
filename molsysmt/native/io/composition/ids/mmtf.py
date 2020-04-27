def from_mmtf(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.ids.api_pdb import to_mmtf_MMTFDecoder as mmtf_to_mmtf_MMTFDecoder
    from molsysmt.native.io.composition.classes import from_mmtf_MMTFDecoder as mmtf_Decoder_to_molsysmt_Composition

    tmp_item = mmtf_to_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all')
    tmp_item = mmtf_Decoder_to_molsysmt_Composition(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

