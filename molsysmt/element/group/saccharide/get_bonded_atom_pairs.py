import numpy as np

from molsysmt._private.smonitor import InternalAlgorithmError

_sorted = sorted


def get_bonded_atom_pairs(group_name, atom_names, atom_indices=None, sorted=True):
    """Getting reference bond index pairs for a named saccharide.

    Parameters
    ----------
    group_name : str
        Exact case-sensitive name in the bundled family catalogue.
    atom_names : list of str, tuple of str, or numpy.ndarray
        One-dimensional names in caller order. Lists, tuples and NumPy arrays
        are equivalent, including empty inputs. Repeated names refer to their
        first occurrence; this helper does not resolve alternate locations.
    atom_indices : list of int, tuple of int, or numpy.ndarray, default=None
        One integer atom index per name, in the same order. If None, use local
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
        For a recognized group, if atom_names is not a flat sequence of strings.
    InternalAlgorithmError
        If the group name is unknown or its atom names match no template layout.

    Notes
    -----
    Unknown group names or a name set matching no stored layout raise
    InternalAlgorithmError. Existing family-specific diagnostics are retained.
    This is a bundled-reference lookup. It neither reads coordinates nor infers
    the graph of a molecular system, assigns chemical state, or adds bonds.
    Caller-owned names and indices are not modified.

    See Also
    --------
    molsysmt.element.group.get_bonded_atom_pairs
    molsysmt.chemical_states.get_bondgraph

    Examples
    --------
    >>> import numpy as np
    >>> from molsysmt.element.group.saccharide import get_bonded_atom_pairs
    >>> get_bonded_atom_pairs('NAG', np.asarray(['C1', 'C2', 'C3']),
    ...                      atom_indices=[20, 10, 30])
    [[10, 20], [10, 30]]
    >>> get_bonded_atom_pairs('NAG', [])
    []

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_bonded_atom_pairs` for mapping and container examples.

    .. versionadded:: 1.0.0
    """

    from . import get_group_db, group_names

    if group_name not in group_names:
        raise InternalAlgorithmError(
            "Unexpected empty state",
            caller="molsysmt.element.group.saccharide.get_bonded_atom_pairs",
        )
    from molsysmt._private.argdigest.argument.atom_names import _flat_atom_name_list

    atom_names = _flat_atom_name_list(
        atom_names, caller=f"{__name__}.get_bonded_atom_pairs"
    )
    if atom_indices is None:
        atom_indices = np.arange(len(atom_names), dtype=int).tolist()

    db = get_group_db(group_name)

    is_in = -1
    for ii, jj in enumerate(db["topology"]):
        if np.all(np.isin(atom_names, jj["atoms"])):
            is_in = ii
            break

    if is_in != -1:
        bonds = []
        for ii, jj in db["topology"][is_in]["bonds"]:
            if ii in atom_names:
                if jj in atom_names:
                    iii = atom_indices[atom_names.index(ii)]
                    jjj = atom_indices[atom_names.index(jj)]
                    if iii < jjj:
                        bonds.append([iii, jjj])
                    else:
                        bonds.append([jjj, iii])

    else:
        print(group_name, atom_names)

        raise InternalAlgorithmError(
            "Unexpected empty state",
            caller="molsysmt.element.group.saccharide.get_bonded_atom_pairs",
        )
    if sorted:
        return _sorted(bonds)
    else:
        return bonds
