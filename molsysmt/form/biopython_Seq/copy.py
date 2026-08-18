from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form biopython.Seq.

    Parameters
    ----------
    item : biopython.Seq
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.Seq
        Copied item.
    """

    return item.copy()

