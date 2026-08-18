from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openmm.GromacsTopFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.GromacsTopFile.

    Parameters
    ----------
    item : openmm.GromacsTopFile
        Source item in openmm.GromacsTopFile form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.GromacsTopFile
        Resulting object in openmm.GromacsTopFile form.

    .. versionadded:: 1.0.0
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

