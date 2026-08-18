from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mdcrd')
def append_structures(to_item, item, structure_indices='all', skip_digestion=False):
    """
    Appending coordinate structures to an item of form file:mdcrd.

    Parameters
    ----------
    item : file:mdcrd
        Target item.
    structure_id : object, optional
        Structure identifier.
    time : object, optional
        Time coordinates.
    coordinates : object, optional
        Cartesian coordinate array in nanometers.
    box : object, optional
        Box vectors in nanometers.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:mdcrd
        Updated item with appended structures.
    """

    raise NotImplementedMethodError()
