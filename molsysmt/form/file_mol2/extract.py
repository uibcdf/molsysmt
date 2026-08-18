from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='file:mol2')
@dep_digest('parmed')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True,
            skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form file:mol2.

    Parameters
    ----------
    item : file:mol2
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:mol2
        Extracted subset in the same form.
    """

    if output_filename is None:
        output_filename = item

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all or (output_filename!=item):

            raise NotImplementedMethodError()

        else:

            raise NotImplementedMethodError()

    else:

        raise NotImplementedMethodError()

