from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:bcif')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:bcif.


    Parameters
    ----------
    item : molecular system
        Argument item.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:bcif
        Resulting object in file:bcif form.


    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        output_filename = item

    raise NotImplementedMethodError()

