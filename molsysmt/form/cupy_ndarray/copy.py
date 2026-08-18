from molsysmt._private.argdigest import arg_digest

@arg_digest(form='cupy_ndarray')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form cupy_ndarray.

    Parameters
    ----------
    item : cupy_ndarray
        Source item in cupy_ndarray form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    cupy_ndarray
        Resulting object in cupy_ndarray form.

    .. versionadded:: 1.0.0
    """
    return item.copy()
