from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='file:h5msm')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):
    """
    Converting from file:h5msm to string:amino_acids_3.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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

    from . import get_group_name_from_group
    from . import get_group_name_from_group

    group_names = get_group_name_from_group(item, indices=group_indices)
    tmp_item = ''.join([ii.title() for ii in group_names])

    return tmp_item

