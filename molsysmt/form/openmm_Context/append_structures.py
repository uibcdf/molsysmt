from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Context')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, skip_digestion=True):
    """
    Appending coordinate structures to an item of form openmm.Context.

    Parameters
    ----------
    item : openmm.Context
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
    openmm.Context
        Updated item with appended structures.
    """

    raise NotImplementedMethodError()

