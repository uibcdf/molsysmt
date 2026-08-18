from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
import types

form = 'mdtraj.Topology'

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting n structures from system in form mdtraj.Topology.

    Parameters
    ----------
    item : mdtraj.Topology
        Source item in mdtraj.Topology form.
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
    raise NotWithThisFormError()

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    """
    Getting coordinates from atom in form mdtraj.Topology.

    Parameters
    ----------
    item : mdtraj.Topology
        Source item in mdtraj.Topology form.
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
    raise NotWithThisFormError()

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting box from system in form mdtraj.Topology.

    Parameters
    ----------
    item : mdtraj.Topology
        Source item in mdtraj.Topology form.
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
    raise NotWithThisFormError()

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
