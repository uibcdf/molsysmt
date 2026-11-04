from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.reference_bonds import DIGEST_OPTIONS

_sorted = sorted


@arg_digest(**DIGEST_OPTIONS)
def get_bonded_atom_pairs(atom_names, atom_indices=None, sorted=True):
    """Getting oxygen-hydrogen reference index pairs for a water group.

    Parameters
    ----------
    atom_names : list of str, tuple of str, or numpy.ndarray
        One-dimensional atom names in caller order. Supply the names for the
        reference layout to query; this is not a molecular-system selection.
        For a complete water query, include one oxygen and at least two
        hydrogens recognizable by their atom names. Extra sites are ignored.
    atom_indices : list of int, tuple of int, or numpy.ndarray, default=None
        One nonnegative integer per supplied name, in the same order. None uses local
        positions 0 through len(atom_names)-1. Explicit indices are mapping
        labels, not positions to select from atom_names or a molecular system.
    sorted : bool, default=True
        Whether to sort pair rows lexicographically. False retains hydrogen
        encounter order. The oxygen endpoint always remains first in each row.

    Returns
    -------
    list of list of int
        Two oxygen-hydrogen pairs using local positions or supplied indices.
        Explicit NumPy indices can remain NumPy integer scalars. Fewer than
        three supplied names return an empty list.

    Raises
    ------
    ArgumentError
        If names or mapped index values violate the flat input contract.
    ArgumentLengthError
        If the explicit map does not contain exactly one index per atom name.

    Notes
    -----
    Maps may contain repeated indices and are not permutations. Values must
    fit int64 and be unit-free and unmasked. Strings, floats, booleans,
    negative indices and nested maps are
    rejected before reference access. An empty name sequence requires an empty
    map or None.

    Oxygen is the first endpoint even if its mapped index is larger than the
    hydrogen index. This differs from the endpoint ordering in stored-template
    helpers. The first two recognized hydrogens in caller order are used.
    Input must describe a water layout; this legacy helper does not validate
    arbitrary molecular compositions or infer a graph from spatial proximity.

    This queries bundled reference connectivity. It does not inspect coordinates,
    infer the graph of a molecular system, assign a chemical state or add bonds.
    Caller-owned names and index maps are not modified. Supply a flat integer
    map with exactly one entry per name when atom_indices is given.

    See Also
    --------
    molsysmt.chemical_states.get_bondgraph
    molsysmt.build.get_missing_bonds

    Examples
    --------
    >>> from molsysmt.element.group.water import get_bonded_atom_pairs
    >>> get_bonded_atom_pairs(['O', 'H1', 'H2'], atom_indices=[1040, 1009, 1030])
    [[1040, 1009], [1040, 1030]]
    >>> get_bonded_atom_pairs([])
    []

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_bonded_atom_pairs` for local and explicit mapping.

    .. versionadded:: 1.0.0
    """

    from molsysmt.element.atom import get_atom_type_from_atom_name

    if len(atom_names) >= 3:
        if atom_indices is None:
            atom_indices = list(range(len(atom_names)))

        oxygen_index = None
        Hs = []

        for atom_index, atom_name in zip(atom_indices, atom_names):
            atom_type = get_atom_type_from_atom_name(atom_name)

            if atom_type == "O":
                oxygen_index = atom_index
            elif atom_type == "H":
                Hs.append(atom_index)

        if sorted:
            return _sorted([[oxygen_index, Hs[0]], [oxygen_index, Hs[1]]])
        else:
            return [[oxygen_index, Hs[0]], [oxygen_index, Hs[1]]]

    else:
        return []
