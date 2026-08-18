from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.Universe')
def to_MDAnalysis_Universe(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from MDAnalysis.Universe to MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    MDAnalysis.Universe
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

