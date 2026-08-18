from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:bcif.gz')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:bcif.gz.

    Parameters
    ----------
    item : file:bcif.gz
        Source item in file:bcif.gz form.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:bcif.gz
        Resulting object in file:bcif.gz form.

    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        output_filename = item

    raise NotImplementedMethodError()

