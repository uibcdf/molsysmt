import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.reference_bonds import DIGEST_OPTIONS


@arg_digest(**DIGEST_OPTIONS)
def get_bonded_atom_pairs(group_name, atom_names, atom_indices=None, sorted=True):
    """Getting reference bond index pairs for a named small molecule.

    Parameters
    ----------
    group_name : str
        Exact case-sensitive name in the bundled family catalogue.
    atom_names : list of str, tuple of str, or numpy.ndarray
        One-dimensional names in caller order. Lists, tuples and NumPy arrays
        are equivalent, including empty inputs. Repeated names refer to their
        first occurrence; this helper does not resolve alternate locations.
    atom_indices : list of int, tuple of int, or numpy.ndarray, default=None
        One nonnegative integer per name, in the same order. If None, use local
        positions 0 through len(atom_names)-1. These are mapping labels, not a
        selection to apply to a molecular system.
    sorted : bool, default=True
        Whether to sort pair rows lexicographically. False retains template
        bond order. Each pair has its smaller mapped endpoint first.

    Returns
    -------
    list of list of int
        Reference bonds whose two names occur in atom_names, mapped to local
        positions or the supplied indices. Explicit NumPy indices may remain
        NumPy integer scalars. An empty name sequence returns an empty list.

    Raises
    ------
    ArgumentError
        If atom_names is not a flat sequence of strings or a map entry is not
        a nonnegative int64-range integer. Booleans are rejected.
    ArgumentLengthError
        If the explicit map does not contain exactly one index per atom name.

    Notes
    -----
    Unknown names and unmatched template layouts return an empty list.
    This is a bundled-reference lookup. It neither reads coordinates nor infers
    the graph of a molecular system, assigns chemical state, or adds bonds.
    Caller-owned names and indices are not modified. Maps may contain repeated
    indices and are not permutations. Values must fit int64 and be unit-free
    and unmasked. Strings, floats,
    booleans, negative indices and nested maps are rejected before reference
    access. An empty name sequence requires an empty map or None.

    See Also
    --------
    molsysmt.element.group.get_bonded_atom_pairs
    molsysmt.chemical_states.get_bondgraph

    Examples
    --------
    >>> import numpy as np
    >>> from molsysmt.element.group.small_molecule import get_bonded_atom_pairs
    >>> get_bonded_atom_pairs('ATP', np.asarray(['PG', 'O1G', 'O2G']),
    ...                      atom_indices=[20, 10, 30])
    [[10, 20], [20, 30]]
    >>> get_bonded_atom_pairs('ATP', [])
    []

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_bonded_atom_pairs` for mapping and container examples.

    .. versionadded:: 1.0.0
    """

    from . import get_group_db, group_names

    if group_name not in group_names:
        return []

    if atom_indices is None:
        atom_indices = np.arange(len(atom_names), dtype=int).tolist()

    db = get_group_db(group_name)

    is_in = -1
    for ii, jj in enumerate(db["topology"]):
        if np.all(np.isin(atom_names, jj["atoms"])):
            is_in = ii
            break

    bonds = []
    if is_in != -1:
        for ii, jj in db["topology"][is_in]["bonds"]:
            if ii in atom_names:
                if jj in atom_names:
                    iii = atom_indices[atom_names.index(ii)]
                    jjj = atom_indices[atom_names.index(jj)]
                    if iii < jjj:
                        bonds.append([iii, jjj])
                    else:
                        bonds.append([jjj, iii])

    if sorted:
        from molsysmt._private.lists import sorted_list_of_pairs

        bonds = sorted_list_of_pairs(bonds)

    return bonds
