from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def merge(items, atom_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form openff.Molecule.


    Parameters
    ----------
    items : object
        Argument items.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openff.Molecule
        Resulting object in openff.Molecule form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
