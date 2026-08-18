from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:cif.gz')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:cif.gz.

    Parameters
    ----------
    item : file:cif.gz
        Source item in file:cif.gz form.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:cif.gz
        Resulting object in file:cif.gz form.

    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        output_filename = item

    raise NotImplementedMethodError()

