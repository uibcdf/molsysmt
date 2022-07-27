from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_biopython_Seq(item, group_indices='all'):

    if check:

        digest_item(item, 'file:inpcrd')
        group_indices = digest_group_indices(group_indices)

    from . import to_string_aminoacids1
    from ..string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    tmp_item = to_string_aminoacids1(item, group_indices=group_indices)
    tmp_item = string_aminoacids1_to_biopython_Seq(tmp_item)

    return tmp_item

