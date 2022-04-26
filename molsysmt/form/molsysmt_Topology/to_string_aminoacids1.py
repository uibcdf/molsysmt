from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_string_aminoacids1(item, group_indices='all', check=True):

    if check:

        digest_item(item, 'molsysmt.Topology')
        group_indices = digest_group_indices(group_indices)

    from . import to_string_aminoacids3
    from ..string_aminoacids3 import to_string_aminoacids1 as string_aminoacids3_to_string_aminoacids1

    tmp_item = to_string_aminoacids3(item, group_indices=group_indices, check=False)
    tmp_item = string_aminoacids3_to_string_aminoacids1(tmp_item, check=False)

    return tmp_item

