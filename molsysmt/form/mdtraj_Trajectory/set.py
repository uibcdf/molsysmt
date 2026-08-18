from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError

form='mdtraj.Trajectory'

@arg_digest(form=form)
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):
    """
    Setting coordinates to atom on form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    value : object, default=None
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()

@arg_digest(form=form)
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):
    """
    Setting box to system on form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    value : object, default=None
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()
