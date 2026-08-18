from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.AmberInpcrdFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.AmberInpcrdFile.

    Parameters
    ----------
    item : openmm.AmberInpcrdFile
        Source item in openmm.AmberInpcrdFile form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.AmberInpcrdFile
        Resulting object in openmm.AmberInpcrdFile form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

