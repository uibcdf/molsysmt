from molsysmt._private.digestion import digest

@digest(form='file:mmtf')
def to_mmtf_MMTFDecoder(item, atom_indices='all', structure_indices='all'):

    from mmtf import parse
    from ..mmtf_MMTFDecoder import extract as extract_mmtf_MMTFDecoder

    tmp_item = parse(item)
    tmp_item = extract_mmtf_MMTFDecoder(tmp_item, atom_indices=atom_indices,
                                        structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

def _to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_mmtf_MMTFDecoder(item, atom_indices=atom_indices, structure_indices=structure_indices)

