from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq')
def to_biopython_Seq(item, group_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from biopython.Seq to biopython.Seq.

    Parameters
    ----------
    item : biopython.Seq
        Source item in biopython.Seq form.
    group_indices : str, list, tuple, or numpy.ndarray, default='all'
        Group indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.Seq
        Resulting object in biopython.Seq form.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(item, group_indices=group_indices, copy_if_all=copy_if_all, skip_digestion=True)

