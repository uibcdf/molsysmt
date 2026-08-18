from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.Universe')
@dep_digest('MDAnalysis')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    MDAnalysis.Universe
        Extracted subset in the same form.
    """

    if is_all(atom_indices) and is_all(structure_indices) and not copy_if_all:
        return item

    from ._subset import subset_universe

    return subset_universe(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
    )
