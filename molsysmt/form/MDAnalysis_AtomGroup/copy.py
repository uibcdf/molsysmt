from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="MDAnalysis.AtomGroup")
@dep_digest("MDAnalysis")
def copy(item, skip_digestion=False):
    """Creating an independent copy of an MDAnalysis atom-group view.

    Parameters
    ----------
    item : molecular system
        Source atom group, retaining its order and parent topology context.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.AtomGroup
        Same ordered atom view backed by an independent parent Universe. Stored
        labels, formal charges, bond metadata and represented structures remain
        available without sharing their arrays with the source.

    Notes
    -----
    The parent is copied through MDAnalysis's independent-copy protocol, so
    unselected parent atoms remain available as context. This does not perceive
    bonds or reinterpret stored bond labels. Arbitrary application attributes
    attached to the group or Universe are outside the provider's copy contract.

    Examples
    --------
    >>> from MDAnalysis import Universe
    >>> source = Universe.empty(2)
    >>> result = copy(source.atoms[[1]])
    >>> result.indices.tolist()
    [1]
    >>> result.universe is source, result.universe.atoms.n_atoms
    (False, 2)

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.MDAnalysis_Universe._subset import copy_universe

    return copy_universe(item.universe).atoms[item.indices]
