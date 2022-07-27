from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_string_aminoacids1(item, group_indices='all'):

    if check:

        digest_item(item, 'molsysmt.Topology')
        group_indices = digest_group_indices(group_indices)

    from . import to_string_aminoacids3
    from ..string_aminoacids3 import to_string_aminoacids1 as string_aminoacids3_to_string_aminoacids1

    tmp_item = to_string_aminoacids3(item, group_indices=group_indices)
    tmp_item = string_aminoacids3_to_string_aminoacids1(tmp_item)

    return tmp_item

