from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:amino_acids_1')
@dep_digest('Bio')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):
    """
    Converting from string:amino_acids_1 to string:amino_acids_3.

    Parameters
    ----------
    item : string:amino_acids_1
        Source item in string:amino_acids_1 form.
    group_indices : str, list, tuple, or numpy.ndarray, default='all'
        Group indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.

    .. versionadded:: 1.0.0
    """

    from Bio.SeqUtils import seq3

    tmp_item=seq3(item)

    return tmp_item
