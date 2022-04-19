from molsysmt._private.digestion import digest_item, digest_group_indices

def to_string_aminoacids1(item, group_indices='all', check=True):

    if check:

        digest_item(item, 'file:mmtf')
        group_indices = digest_group_indices(group_indices)

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_string_aminoacids1 as mmtf_MMTFDecoder_to_string_aminoacids1

    tmp_item = to_mmtf_MMTFDecoder(item, check=False)
    tmp_item = mmtf_MMTFDecoder_to_string_aminoacids1(tmp_item, group_indices=group_indices, check=False)

    return tmp_item

