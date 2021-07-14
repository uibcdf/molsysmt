def from_string_pdbid(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.string.api_string_pdbid import to_mmtf_MMTFDecoder as string_pdbid_to_mmtf_MMTFDecoder
    from molsysmt.native.io.topology.classes import from_mmtf_MMTFDecoder as mmtf_Decoder_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = string_pdbid_to_mmtf_MMTFDecoder(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = mmtf_Decoder_to_molsysmt_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

