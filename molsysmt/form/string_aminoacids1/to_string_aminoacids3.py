from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='string:aminoacids1')
def to_string_aminoacids3(item, group_indices='all'):

    try:
        from Bio.SeqUtils import seq3
    except:
        raise LibraryNotFoundError('biopython')

    tmp_item=seq3(item)

    return tmp_item

def _to_string_aminoacids3(item, atom_indices='all', structure_indices='all'):

    return to_string_aminoacids3(item)

