from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:amino_acids_3')
def to_biopython_SeqRecord(item, group_indices='all', skip_digestion=False):

    from .to_string_amino_acids_1 import to_string_amino_acids_1
    from ..string_amino_acids_1.to_biopython_SeqRecord import to_biopython_SeqRecord as string_amino_acids_1_to_biopython_SeqRecord

    tmp_item = to_string_amino_acids_1(item, group_indices=group_indices, skip_digestion=True)
    tmp_item = string_amino_acids_1_to_biopython_SeqRecord(tmp_item, skip_digestion=True)

    return tmp_item

