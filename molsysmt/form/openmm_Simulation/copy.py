from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.Simulation.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Simulation
        Resulting object in openmm.Simulation form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

