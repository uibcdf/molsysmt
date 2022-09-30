from molsysmt._private.digestion import digest

@digest(form='file:mmtf')
def to_string_aminoacids3(item, group_indices='all'):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_string_aminoacids3 as mmtf_MMTFDecoder_to_string_aminoacids3

    tmp_item = to_mmtf_MMTFDecoder(item)
    tmp_item = mmtf_MMTFDecoder_to_string_aminoacids3(tmp_item, group_indices=group_indices)

    return tmp_item

