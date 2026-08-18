from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:amino_acids_1')
@dep_digest('Bio')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):
    """
    Converting from string:amino_acids_1 to string.amino.acids.3.

    Parameters
    ----------
    item : string:amino_acids_1
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.amino.acids.3
        Converted molecular system representation.
    """

    from Bio.SeqUtils import seq3

    tmp_item=seq3(item)

    return tmp_item
