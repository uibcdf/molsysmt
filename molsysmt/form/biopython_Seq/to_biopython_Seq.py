from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq')
def to_biopython_Seq(item, group_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from biopython.Seq to biopython.Seq.

    Parameters
    ----------
    item : biopython.Seq
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.Seq
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, group_indices=group_indices, copy_if_all=copy_if_all, skip_digestion=True)

