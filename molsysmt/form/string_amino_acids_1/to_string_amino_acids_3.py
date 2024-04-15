from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='string:amino_acids_1')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):

    try:
        from Bio.SeqUtils import seq3
    except:
        raise LibraryNotFoundError('biopython')

    tmp_item=seq3(item)

    return tmp_item

