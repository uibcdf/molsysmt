from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.SeqRecord')
def to_biopython_SeqRecord(item, group_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from biopython.SeqRecord to biopython.SeqRecord.

    Parameters
    ----------
    item : biopython.SeqRecord
        Source item in biopython.SeqRecord form.
    group_indices : str, list, tuple, or numpy.ndarray, default='all'
        Group indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.SeqRecord
        Resulting object in biopython.SeqRecord form.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(item, group_indices=group_indices, copy_if_all=copy_if_all, skip_digestion=True)

