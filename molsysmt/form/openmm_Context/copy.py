from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@arg_digest(form="openmm.Context")
def copy(item):
    """
    Requesting an independent copy of an OpenMM Context.


    Parameters
    ----------
    item : molecular system
        Argument item.

    Returns
    -------
    openmm.Context
        The requested independent context. This operation is currently
        unsupported and raises without returning a result.

    Raises
    ------
    NotImplementedMethodError
        Independent Context copying is not implemented. The input is unchanged.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError(
        method="independent copy of openmm.Context",
        arguments={"form": "openmm.Context"},
        caller="molsysmt.form.openmm_Context.copy",
    )
