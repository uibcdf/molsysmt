from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pytraj.Trajectory', to_form='pytraj.Trajectory')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form pytraj.Trajectory.

    Parameters
    ----------
    to_item : pytraj.Trajectory
        Target item to modify or add elements to.
    item : pytraj.Trajectory
        Source item in pytraj.Trajectory form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    pytraj.Trajectory
        Resulting object in pytraj.Trajectory form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

