from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.SeqRecord')
def to_biopython_SeqRecord(item, group_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from biopython.SeqRecord to biopython.SeqRecord.

    Parameters
    ----------
    item : biopython.SeqRecord
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.SeqRecord
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, group_indices=group_indices, copy_if_all=copy_if_all, skip_digestion=True)

