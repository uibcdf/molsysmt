from molsysmt.dependencies import requires
from molsysmt._private.digestion import digest

@digest(form='string:amino_acids_1')
@requires('biopython')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):

    from Bio.SeqUtils import seq3

    tmp_item=seq3(item)

    return tmp_item

