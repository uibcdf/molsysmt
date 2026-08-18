from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5msm', to_form='file:h5msm')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form file:h5msm.

    Parameters
    ----------
    to_item : file:h5msm
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:h5msm
        Target item with added elements.
    """

    raise NotImplementedMethodError()

