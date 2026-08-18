from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import types

form='molsysmt.Structures'

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom index from atom in form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices is None:
        return None
    if is_all(indices):
        return list(range(item.coordinates.shape[1]))
    return list(indices)


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.coordinates.shape[1]

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
