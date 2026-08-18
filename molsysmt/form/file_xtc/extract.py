from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='file:xtc')
@dep_digest('mdtraj')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True,
            skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form file:xtc.

    Parameters
    ----------
    item : file:xtc
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:xtc
        Extracted subset in the same form.
    """

    if output_filename is None:
        output_filename = item

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all or (output_filename!=item):

            from shutil import copy as copy_file
            copy_file(item, output_filename)
            tmp_item = output_filename

        else:

            tmp_item = item
    else:

        raise NotImplementedError()

    return tmp_item

