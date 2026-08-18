from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import types

form = 'molsysmt.PDBFileHandler'


def _get_models(item):
    models = item.entry.coordinate.model
    if models is None:
        return []
    return models


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    """
    Getting coordinates from atom in form molsysmt.PDBFileHandler.

    Parameters
    ----------
    item : molsysmt.PDBFileHandler
        Source item in molsysmt.PDBFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures import get_coordinates_from_atom as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting n structures from system in form molsysmt.PDBFileHandler.

    Parameters
    ----------
    item : molsysmt.PDBFileHandler
        Source item in molsysmt.PDBFileHandler form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if is_all(structure_indices):
        return max(len(_get_models(item)), 1)
    return len(structure_indices)


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting box from system in form molsysmt.PDBFileHandler.

    Parameters
    ----------
    item : molsysmt.PDBFileHandler
        Source item in molsysmt.PDBFileHandler form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures import get_box_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting time from system in form molsysmt.PDBFileHandler.

    Parameters
    ----------
    item : molsysmt.PDBFileHandler
        Source item in molsysmt.PDBFileHandler form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures import get_time_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting structure id from system in form molsysmt.PDBFileHandler.

    Parameters
    ----------
    item : molsysmt.PDBFileHandler
        Source item in molsysmt.PDBFileHandler form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures import get_structure_id_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
