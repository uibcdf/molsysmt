from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.State', to_form='openmm.State')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form openmm.State.

    Parameters
    ----------
    to_item : openmm.State
        Target item to modify or add elements to.
    item : openmm.State
        Source item in openmm.State form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.State
        Resulting object in openmm.State form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

