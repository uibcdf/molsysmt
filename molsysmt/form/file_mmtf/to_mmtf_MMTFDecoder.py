from molsysmt._private.digestion import digest

@digest(form='file:mmtf')
def to_mmtf_MMTFDecoder(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from mmtf import parse
    from ..mmtf_MMTFDecoder import extract as extract_mmtf_MMTFDecoder

    tmp_item = parse(item)
    tmp_item = extract_mmtf_MMTFDecoder(tmp_item, atom_indices=atom_indices,
                                        structure_indices=structure_indices, copy_if_all=False,
                                        skip_digestion=True)

    return tmp_item

