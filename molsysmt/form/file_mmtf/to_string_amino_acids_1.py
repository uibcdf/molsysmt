from molsysmt._private.arg_digestion import arg_digest
import numpy as np

@arg_digest(form='file:mmtf')
def to_string_amino_acids_1(item, group_indices='all', skip_digestion=False):

    from .to_mmtf_MMTFDecoder import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder.to_string_amino_acids_1 import to_string_amino_acids_1 as mmtf_MMTFDecoder_to_string_amino_acids_1

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    tmp_item = mmtf_MMTFDecoder_to_string_amino_acids_1(tmp_item, group_indices=group_indices, skip_digestion=True)

    return tmp_item
