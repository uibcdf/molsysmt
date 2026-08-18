from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='file:h5msm')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):
    """
    Converting from file:h5msm to string.amino.acids.3.

    Parameters
    ----------
    item : file:h5msm
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.amino.acids.3
        Converted molecular system representation.
    """

    from . import get_group_name_from_group
    from . import get_group_name_from_group

    group_names = get_group_name_from_group(item, indices=group_indices)
    tmp_item = ''.join([ii.title() for ii in group_names])

    return tmp_item

