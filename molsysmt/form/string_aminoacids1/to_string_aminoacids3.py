from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_string_aminoacids3(item, group_indices='all', check=True):

    if check:

        digest_item(item, 'string:aminoacids1')
        group_indices = digest_group_indices(group_indices)

    try:
        from Bio.SeqUtils import seq3
    except:
        raise LibraryNotFoundError('biopython')

    tmp_item=seq3(item)

    return tmp_item

