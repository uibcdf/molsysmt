from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openmm.PDBFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.PDBFile.

    Parameters
    ----------
    item : openmm.PDBFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.PDBFile
        Copied item.
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

