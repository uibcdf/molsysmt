from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.Universe')
@dep_digest('MDAnalysis')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item in MDAnalysis.Universe form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.Universe
        Resulting object in MDAnalysis.Universe form.

    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices) and not copy_if_all:
        return item

    from ._subset import subset_universe

    return subset_universe(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
    )
