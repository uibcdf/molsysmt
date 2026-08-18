from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, skip_digestion=False):
    """
    Appending coordinate structures to an item of form file:mol2.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_id : object, default=None
        Argument structure_id.
    time : object, default=None
        Argument time.
    coordinates : object, default=None
        Argument coordinates.
    box : object, default=None
        Argument box.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:mol2
        Resulting object in file:mol2 form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

