from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='string:amino_acids_1')
@dep_digest('Bio')
def to_biopython_Seq(item, group_indices='all', skip_digestion=False):

    from Bio.Seq import Seq as bio_Seq

    if not is_all(group_indices):
        item = ''.join(item[index] for index in group_indices)

    tmp_item = bio_Seq(item)

    return tmp_item
