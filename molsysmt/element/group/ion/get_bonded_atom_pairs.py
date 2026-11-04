import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    InternalAlgorithmError,
)

_sorted = sorted


@arg_digest()
def get_bonded_atom_pairs(
    group_name, atom_names, atom_indices=None, sorted=True, skip_digestion=False
):
    """Getting reference bond index pairs for an ion group.

    Parameters
    ----------
    group_name : str
        Case-sensitive ion name in the bundled reference catalogue.
    atom_names : str, list of str, tuple of str, or numpy.ndarray
        One-dimensional atom names in caller order. Supply the names for the
        reference layout to query; this is not a molecular-system selection.
        A single atom-name string is accepted as a one-atom query. Repeated
        names use their first occurrence in the supplied sequence.
    atom_indices : int, list of int, tuple of int, or numpy.ndarray, default=None
        One integer index per supplied name, in the same order. None uses local
        positions 0 through len(atom_names)-1. Explicit indices are mapping
        labels, not positions to select from atom_names or a molecular system.
        A scalar integer is also accepted for a single supplied name.
    sorted : bool, default=True
        Whether to sort pair rows lexicographically. False retains reference
        bond order. Each pair has its smaller mapped endpoint first.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of list of int or None
        Reference bonds mapped to integer atom indices. Explicit maps are
        normalized to NumPy integer scalars. A one-atom query returns an empty
        list without consulting the group catalogue. Empty names return an
        empty list for a recognized group. Unmatched multi-atom layouts return
        None.

    Raises
    ------
    ArgumentError
        If the argument digester rejects an input value.
    InternalAlgorithmError
        If a query other than the one-atom shortcut uses an unknown group name.

    Notes
    -----
    The one-atom shortcut describes an isolated ion and does not test whether
    group_name is in the reference catalogue. For multi-atom groups, names are
    checked against the available reference layouts before mapping their edges.

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
    >>> from molsysmt.element.group.ion import get_bonded_atom_pairs
    >>> pairs = get_bonded_atom_pairs('SO4', ['S', 'O1', 'O2'],
    ...                              atom_indices=[20, 10, 30])
    >>> [[int(index) for index in pair] for pair in pairs]
    [[10, 20], [20, 30]]
    >>> get_bonded_atom_pairs('K', 'K')
    []

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_bonded_atom_pairs` for local and explicit mapping.

    .. versionadded:: 1.0.0
    """

    n_atoms = len(atom_names)

    if n_atoms == 1:
        return []

    else:
        from molsysmt.element.group.ion import get_group_db, group_names

        if group_name not in group_names:
            raise InternalAlgorithmError(
                "Unexpected empty state",
                caller="molsysmt.element.group.ion.get_bonded_atom_pairs",
            )
        if atom_indices is None:
            atom_indices = np.arange(len(atom_names), dtype=int).tolist()

        aux_group_names = [group_name]

        for aux_group_name in aux_group_names:
            db = get_group_db(aux_group_name)

            is_in = -1
            for ii, jj in enumerate(db["atom_name"]):
                if np.all(np.isin(atom_names, jj)):
                    is_in = ii
                    break

            if is_in != -1:
                bonds = []
                for i, j in db["bonds"]:
                    ii = db["atom_name"][is_in][i]
                    jj = db["atom_name"][is_in][j]
                    if ii in atom_names:
                        if jj in atom_names:
                            iii = atom_indices[atom_names.index(ii)]
                            jjj = atom_indices[atom_names.index(jj)]
                            if iii < jjj:
                                bonds.append([iii, jjj])
                            else:
                                bonds.append([jjj, iii])
                if sorted:
                    return _sorted(bonds)
                else:
                    return bonds
