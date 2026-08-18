from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.GromacsTopFile', to_form='openmm.GromacsTopFile')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form openmm.GromacsTopFile.

    Parameters
    ----------
    to_item : openmm.GromacsTopFile
        Target item to modify or add elements to.
    item : openmm.GromacsTopFile
        Source item in openmm.GromacsTopFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.GromacsTopFile
        Resulting object in openmm.GromacsTopFile form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()


