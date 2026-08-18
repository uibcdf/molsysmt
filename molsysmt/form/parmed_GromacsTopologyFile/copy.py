from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.GromacsTopologyFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form parmed.GromacsTopologyFile.

    Parameters
    ----------
    item : parmed.GromacsTopologyFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    parmed.GromacsTopologyFile
        Copied item.
    """

    raise NotImplementedMethodError()
