from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='string:amino_acids_1')
@dep_digest('Bio')
def to_biopython_Seq(item, group_indices='all', skip_digestion=False):
    """
    Converting from string:amino_acids_1 to biopython.Seq.


    Parameters
    ----------
    item : molecular system
        Argument item.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Argument group_indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.Seq
        Resulting object in biopython.Seq form.


    .. versionadded:: 1.0.0
    """

    from Bio.Seq import Seq as bio_Seq

    if not is_all(group_indices):
        item = ''.join(item[index] for index in group_indices)

    tmp_item = bio_Seq(item)

    return tmp_item
