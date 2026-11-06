from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@arg_digest(form="openmm.Simulation")
def copy(item, skip_digestion=False):
    """
    Requesting an independent copy of an OpenMM Simulation.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Simulation
        The requested independent simulation. This operation is currently
        unsupported and raises without returning a result.

    Raises
    ------
    NotImplementedMethodError
        Independent Simulation copying is not implemented. The input is unchanged.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError(
        method="independent copy of openmm.Simulation",
        arguments={"form": "openmm.Simulation"},
        caller="molsysmt.form.openmm_Simulation.copy",
    )
