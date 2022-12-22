from molsysmt._private.digestion import digest

@digest(form='file:mmtf')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', digest=True):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_molsysmt_Structures as mmtf_MMTFDecoder_to_molsysmt_Structures

    tmp_item = to_mmtf_MMTFDecoder(item, digest=False)
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)

    return tmp_item

