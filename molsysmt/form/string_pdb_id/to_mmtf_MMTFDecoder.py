from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_mmtf_MMTFDecoder(item, atom_indices='all', structure_indices='all', digest=True):

    from mmtf import fetch
    from ..mmtf_MMTFDecoder import extract as extract_mmtf_MMTFDecoder

    tmp_item = item.split(':')[-1]
    tmp_item = fetch(tmp_item)
    tmp_item = extract_mmtf_MMTFDecoder(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False, digest=False)

    return tmp_item

