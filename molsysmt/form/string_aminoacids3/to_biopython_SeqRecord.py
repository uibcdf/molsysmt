from molsysmt._private.digestion import digest

@digest(form='string:aminoacids3')
def to_biopython_SeqRecord(item, group_indices='all', skip_digestion=False):

    from . import to_string_aminoacids1
    from ..string_aminoacids1 import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    tmp_item = to_string_aminoacids1(item, group_indices=group_indices, skip_digestion=True)
    tmp_item = string_aminoacids1_to_biopython_SeqRecord(tmp_item, skip_digestion=True)

    return tmp_item

