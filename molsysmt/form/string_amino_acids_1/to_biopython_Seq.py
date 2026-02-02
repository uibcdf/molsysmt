from molsysmt.dependencies import requires
from molsysmt._private.digestion import digest

@digest(form='string:amino_acids_1')
@requires('biopython')
def to_biopython_Seq(item, group_indices='all', skip_digestion=False):

    from Bio.Seq import Seq as bio_Seq

    #tmp_item = bio_Seq(item, ExtendedIUPACProtein())
    tmp_item = bio_Seq(item)

    return tmp_item

