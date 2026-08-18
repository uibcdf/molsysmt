from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.GROFileHandler')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form molsysmt.GROFileHandler.

    Parameters
    ----------
    item : molsysmt.GROFileHandler
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.GROFileHandler
        Extracted subset in the same form.
    """

    raise NotImplementedMethodError()

