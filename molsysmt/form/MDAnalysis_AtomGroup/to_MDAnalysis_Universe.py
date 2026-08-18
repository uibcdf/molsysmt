from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.AtomGroup')
def to_MDAnalysis_Universe(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from MDAnalysis.AtomGroup to MDAnalysis.Universe.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.Universe
        Resulting object in MDAnalysis.Universe form.


    .. versionadded:: 1.0.0
    """

    from molsysmt._private.variables import is_all

    indices = item.indices
    if not is_all(atom_indices):
        indices = indices[atom_indices]

    from molsysmt.form.MDAnalysis_Universe._subset import subset_universe

    return subset_universe(
        item.universe,
        atom_indices=indices,
        structure_indices=structure_indices,
    )
