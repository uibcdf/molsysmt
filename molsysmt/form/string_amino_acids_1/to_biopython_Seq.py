from molsysmt.dependencies import dep_digest
from molsysmt._private.digestion import arg_digest

@arg_digest(form='string:amino_acids_1')
@dep_digest('biopython')
def to_biopython_Seq(item, group_indices='all', skip_digestion=False):

    from Bio.Seq import Seq as bio_Seq

    #tmp_item = bio_Seq(item, ExtendedIUPACProtein())
    tmp_item = bio_Seq(item)

    return tmp_item

