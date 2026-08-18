from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.SeqRecord', to_form='biopython.SeqRecord')
def add(to_item, item, group_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form biopython.SeqRecord.

    Parameters
    ----------
    to_item : biopython.SeqRecord
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.SeqRecord
        Target item with added elements.
    """

    raise NotImplementedMethodError()

