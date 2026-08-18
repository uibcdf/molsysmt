from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.SeqRecord')
def to_biopython_SeqRecord(item, group_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from biopython.SeqRecord to biopython.SeqRecord.


    Parameters
    ----------
    item : molecular system
        Argument item.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Argument group_indices.
    copy_if_all : object, default=True
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

