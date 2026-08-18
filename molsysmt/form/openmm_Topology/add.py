from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology', to_form='openmm.Topology')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form openmm.Topology.

    Parameters
    ----------
    to_item : openmm.Topology
        Target item to modify or add elements to.
    item : openmm.Topology
        Source item in openmm.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

