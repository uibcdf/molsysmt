from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:prmtop.


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
    file:prmtop
        Resulting object in file:prmtop form.


    .. versionadded:: 1.0.0
    """

    from shutil import copy as copy_file
    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item

