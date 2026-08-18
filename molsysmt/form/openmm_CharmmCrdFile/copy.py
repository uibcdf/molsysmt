from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.CharmmCrdFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.CharmmCrdFile.

    Parameters
    ----------
    item : openmm.CharmmCrdFile
        Source item in openmm.CharmmCrdFile form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.CharmmCrdFile
        Resulting object in openmm.CharmmCrdFile form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

