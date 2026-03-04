from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:mmtf')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_mmtf_MMTFDecoder import to_mmtf_MMTFDecoder
    from molsysmt.form.mmtf_MMTFDecoder.to_molsysmt_Structures import to_molsysmt_Structures as mmtf_MMTFDecoder_to_molsysmt_Structures

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices,
                                                       structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

