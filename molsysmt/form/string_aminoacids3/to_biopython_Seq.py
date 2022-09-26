from molsysmt._private.digestion import digest

@digest(form='string:aminoacids3')
def to_biopython_Seq(item, group_indices='all', structure_indices='all'):

    from . import to_string_aminoacids1
    from ..string_aminoacids1 import to_biopython_Seq

    tmp_item = to_string_aminoacids1(item, group_indices=group_indices)
    tmp_item = string_aminoacids1_to_biopython_Seq(tmp_item)

    return tmp_item

