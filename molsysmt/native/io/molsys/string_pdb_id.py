def from_string_pdb_id(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_string_pdb_id import to_mmtf_MMTFDecoder as string_pdb_id_to_mmtf_MMTFDecoder
    from molsysmt.native.io.molsys import from_mmtf_MMTFDecoder as mmtf_Decoder_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = string_pdb_id_to_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices='all', frame_indices='all')
    tmp_item, tmp_molecular_system = mmtf_Decoder_to_molsysmt_MolSys(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system


