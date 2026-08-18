from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.CharmmPsfFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.CharmmPsfFile.

    Parameters
    ----------
    item : openmm.CharmmPsfFile
        Source item in openmm.CharmmPsfFile form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.CharmmPsfFile
        Resulting object in openmm.CharmmPsfFile form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

