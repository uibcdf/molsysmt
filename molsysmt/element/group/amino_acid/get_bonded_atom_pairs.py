import numpy as np

from molsysmt._private.argdigest import arg_digest

_sorted = sorted


@arg_digest()
def get_bonded_atom_pairs(
    group_name, atom_names, atom_indices=None, sorted=True, skip_digestion=False
):
    """Getting reference bond index pairs for an amino-acid group.

    Parameters
    ----------
    group_name : str
        Case-sensitive amino-acid name in the bundled reference catalogue.
    atom_names : str, list of str, tuple of str, or numpy.ndarray
        One-dimensional atom names in caller order. Supply the names for the
        reference layout to query; this is not a molecular-system selection.
        A single atom-name string is accepted as a one-atom query. Repeated
        names retain all supplied occurrences; they are not alternate-location
        filtering instructions.
    atom_indices : int, list of int, tuple of int, or numpy.ndarray, default=None
        One integer index per supplied name, in the same order. None uses local
        positions 0 through len(atom_names)-1. Explicit indices are mapping
        labels, not positions to select from atom_names or a molecular system.
        A scalar integer is also accepted for a single supplied name.
    sorted : bool, default=True
        Whether to sort pair rows lexicographically. False retains template
        bond order. Each pair has its smaller mapped endpoint first.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of list of int or None
        Reference bonds with both names present, mapped to the supplied indices
        or local positions. Explicit maps are normalized to NumPy integer
        scalars. Empty names return an empty list for a recognized group.
        Unknown names and unmatched reference layouts return None.

    Raises
    ------
    ArgumentError
        If the argument digester rejects an input value.

    Notes
    -----
    Matching includes the available terminal reference variants. If names repeat,
    each reference edge expands over the corresponding supplied occurrences.
    This preserves the existing lookup behavior and does not establish which
    alternate locations should coexist. Unmatched layouts retain their legacy
    warning and None result.

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
    >>> from molsysmt.element.group.amino_acid import get_bonded_atom_pairs
    >>> pairs = get_bonded_atom_pairs('ALA', ['N', 'CA', 'C', 'O', 'CB'],
    ...                              atom_indices=[1040, 1009, 1030, 1007, 1012])
    >>> [[int(index) for index in pair] for pair in pairs]
    [[1007, 1030], [1009, 1012], [1009, 1030], [1009, 1040]]
    >>> get_bonded_atom_pairs('ALA', [])
    []

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_bonded_atom_pairs` for local and explicit mapping.

    .. versionadded:: 1.0.0
    """

    from molsysmt.element.group.amino_acid import get_group_db, group_names

    if group_name not in group_names:
        return None

    if atom_indices is None:
        atom_indices = np.arange(len(atom_names), dtype=int).tolist()

    aux_group_names = [group_name]

    if "C" + group_name in group_names:
        aux_group_names.append("C" + group_name)

    if "N" + group_name in group_names:
        aux_group_names.append("N" + group_name)

    aux_dict = {}
    for ii, jj in zip(atom_names, atom_indices):
        if ii not in aux_dict:
            aux_dict[ii] = [jj]
        else:
            aux_dict[ii].append(jj)

    for aux_group_name in aux_group_names:
        db = get_group_db(aux_group_name)

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
                        for iii in aux_dict[ii]:
                            for jjj in aux_dict[jj]:
                                if iii < jjj:
                                    bonds.append([iii, jjj])
                                else:
                                    bonds.append([jjj, iii])
            if sorted:
                return _sorted(bonds)
            else:
                return bonds

    if group_name in ["HIS"]:
        for aux_group_name in group_names:
            try:
                db = get_group_db(aux_group_name)
                for ii, jj in enumerate(db["topology"]):
                    if len(atom_names) == len(jj["atoms"]):
                        if np.all(np.isin(atom_names, jj["atoms"])):
                            if np.all(np.isin(jj["atoms"], atom_names)):
                                bonds = []
                                for aa, bb in jj["bonds"]:
                                    if aa in atom_names:
                                        if bb in atom_names:
                                            iii = atom_indices[atom_names.index(aa)]
                                            jjj = atom_indices[atom_names.index(bb)]
                                            if iii < jjj:
                                                bonds.append([iii, jjj])
                                            else:
                                                bonds.append([jjj, iii])
                                if sorted:
                                    return _sorted(bonds)
                                else:
                                    return bonds

            except Exception:
                pass

    print(f"Warning! The amino acid {group_name} has no template.")
    print("No bonds were added by element.group.amino_acid.get_bonded_atom_pairs")

    return None
