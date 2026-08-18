from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.GROFileHandler')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, skip_digestion=False):
    """
    Appending coordinate structures to an item of form molsysmt.GROFileHandler.

    Parameters
    ----------
    item : molsysmt.GROFileHandler
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
    molsysmt.GROFileHandler
        Updated item with appended structures.
    """

    raise NotImplementedMethodError()

