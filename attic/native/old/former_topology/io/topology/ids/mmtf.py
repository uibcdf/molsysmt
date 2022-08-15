def from_mmtf(item, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.ids.api_pdb import to_mmtf_MMTFDecoder as mmtf_to_mmtf_MMTFDecoder
    from molsysmt.native.io.topology import from_mmtf_MMTFDecoder as mmtf_Decoder_to_molsysmt_Topology

    tmp_item = mmtf_to_mmtf_MMTFDecoder(item, atom_indices='all', structure_indices='all')
    tmp_item = mmtf_Decoder_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

