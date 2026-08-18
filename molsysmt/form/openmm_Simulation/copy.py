from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.Simulation.

    Parameters
    ----------
    item : openmm.Simulation
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Simulation
        Copied item.
    """

    raise NotImplementedMethodError()

