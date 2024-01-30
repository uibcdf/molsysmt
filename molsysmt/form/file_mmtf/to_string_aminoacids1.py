from molsysmt._private.digestion import digest
import numpy as np

@digest(form='file:mmtf')
def to_string_aminoacids1(item, group_indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_string_aminoacids1 as mmtf_MMTFDecoder_to_string_aminoacids1

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    tmp_item = mmtf_MMTFDecoder_to_string_aminoacids1(tmp_item, group_indices=group_indices, skip_digestion=True)

    return tmp_item
