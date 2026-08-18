from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq', to_form='biopython.Seq')
def add(to_item, item, group_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form biopython.Seq.

    Parameters
    ----------
    to_item : biopython.Seq
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.Seq
        Target item with added elements.
    """

    raise NotImplementedMethodError()

