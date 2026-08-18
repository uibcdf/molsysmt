from molsysmt._private.argdigest import arg_digest
import importlib
import numpy as np
import types

from ._delegated_getter import make_delegated_getter

form = "molsysmt.MolSysBuilder"


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.topology.n_atoms


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting n structures from system in form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
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
    if structure_indices == "all":
        return item.n_structures
    return len(structure_indices)


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting structure id from system in form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
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
    values = item.structures.structure_id
    if values is None:
        return []
    values = np.asarray(values)
    if structure_indices == "all":
        return values.tolist()
    return values[structure_indices].tolist()


@arg_digest(form=form)
def get_time_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting time from system in form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
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
    values = item.structures.time
    if values is None:
        return None
    if structure_indices == "all":
        return values
    return values[structure_indices]


@arg_digest(form=form)
def get_box_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting box from system in form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
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
    values = item.structures.box
    if values is None:
        return None
    if structure_indices == "all":
        return values
    return values[structure_indices]


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting coordinates from system in form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
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
    values = item.structures.coordinates
    if values is None:
        return None
    if structure_indices == "all":
        return values
    return values[structure_indices]


_target_module = importlib.import_module(
    "molsysmt.form.molsysmt_Structures.get_structural_attributes"
)
for _name in _target_module.__all__:
    if _name not in globals():
        globals()[_name] = make_delegated_getter(
            _name,
            getattr(_target_module, _name),
            "structures",
        )

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith("get_")]

del _name, _target_module
