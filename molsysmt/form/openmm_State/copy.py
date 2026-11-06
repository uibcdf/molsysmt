from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@arg_digest(form="openmm.State")
def copy(item, skip_digestion=False):
    """
    Requesting an independent copy of an OpenMM State snapshot.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.State
        The requested independent snapshot. This operation is currently
        unsupported and raises without returning a result.

    Raises
    ------
    NotImplementedMethodError
        State copying is not implemented. The captured snapshot is unchanged.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError(
        method="independent copy of openmm.State",
        arguments={"form": "openmm.State"},
        caller="molsysmt.form.openmm_State.copy",
    )
