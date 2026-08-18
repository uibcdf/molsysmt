from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form biopython.Seq.

    Parameters
    ----------
    item : biopython.Seq
        Source item in biopython.Seq form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.Seq
        Resulting object in biopython.Seq form.

    .. versionadded:: 1.0.0
    """

    return item.copy()

