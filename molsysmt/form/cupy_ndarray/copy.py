from molsysmt._private.argdigest import arg_digest

@arg_digest(form='cupy_ndarray')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form cupy_ndarray.

    Parameters
    ----------
    item : cupy_ndarray
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    cupy_ndarray
        Copied item.
    """
    return item.copy()
