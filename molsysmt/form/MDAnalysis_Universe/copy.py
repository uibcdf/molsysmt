from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="MDAnalysis.Universe")
@dep_digest("MDAnalysis")
def copy(item, skip_digestion=False):
    """
    Creating an independent copy of a stored MDAnalysis Universe.

    Parameters
    ----------
    item : molecular system
        Source Universe, including its declared topology and available structures.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.Universe
        Independent provider copy preserving topology attributes, bond metadata
        and represented coordinates, velocities, forces, cells and time.

    Notes
    -----
    The source reader and its current structure remain unchanged. This operation
    uses the provider's independent-copy protocol without chemical reconstruction
    or bond perception. Arbitrary application attributes attached to a Universe
    are outside the provider's copy contract.

    Examples
    --------
    >>> from MDAnalysis import Universe
    >>> source = Universe.empty(2)
    >>> result = copy(source)
    >>> result is source, result.atoms.n_atoms
    (False, 2)
    >>> hasattr(result, "trajectory")
    False

    .. versionadded:: 1.0.0
    """

    from ._subset import copy_universe

    return copy_universe(item)
