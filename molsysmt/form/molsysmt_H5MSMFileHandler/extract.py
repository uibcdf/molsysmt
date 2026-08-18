from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.H5MSMFileHandler')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.H5MSMFileHandler
        Extracted subset in the same form.
    """

    if is_all(atom_indices) and is_all(structure_indices):

        if output_filename is not None and output_filename != item:
            from shutil import copy as copy_file
            copy_file(item, output_filename)
            tmp_item = output_filename
        else:
            if copy_if_all and output_filename is not None:
                 from shutil import copy as copy_file
                 copy_file(item, output_filename)
                 tmp_item = output_filename
            else:
                 tmp_item = item
    else:

        raise NotImplementedMethodError()

    return tmp_item

