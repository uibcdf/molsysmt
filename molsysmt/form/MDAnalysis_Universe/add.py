from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.Universe', to_form='MDAnalysis.Universe')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form MDAnalysis.Universe.

    Parameters
    ----------
    to_item : MDAnalysis.Universe
        Target item to modify or add elements to.
    item : MDAnalysis.Universe
        Source item in MDAnalysis.Universe form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.Universe
        Resulting object in MDAnalysis.Universe form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

