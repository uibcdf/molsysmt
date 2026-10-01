"""Packing variable-length integer memberships without padded arrays."""

import numpy as np


def pack_membership(groups):
    """Pack index groups into int64 values and offsets, including empty input."""
    offsets = np.zeros(len(groups) + 1, dtype=np.int64)
    np.cumsum([len(group) for group in groups], out=offsets[1:])
    return np.asarray(
        [atom for group in groups for atom in group], dtype=np.int64
    ), offsets


def whole_group_selection(groups, selected, *, caller, argument="selection", description="compound participant"):
    """Select complete compound participants, rejecting partial intersections."""
    from molsysmt._private.smonitor import ArgumentError

    selected = set(np.asarray(selected).tolist())
    result = np.zeros(len(groups), dtype=bool)
    for index, atoms in enumerate(groups):
        overlap = selected.intersection(atoms.tolist())
        if overlap and len(overlap) != len(atoms):
            raise ArgumentError(argument, caller=caller,
                                message=f"The selection cuts a {description}; include all its atoms.")
        result[index] = bool(overlap)
    return result


def connected_group_pairs(groups, covalent_pairs):
    """Find overlapping or directly bonded groups without an all-group pair matrix.

    Memberships may overlap. Returned unordered pairs exclude self-pairs.
    Cost follows memberships and the multiplicity of groups at bonded atoms.
    """
    from itertools import combinations, product

    by_atom = {}
    for group, atoms in enumerate(groups):
        for atom in atoms:
            by_atom.setdefault(int(atom), []).append(group)
    excluded = {pair for memberships in by_atom.values()
                for pair in combinations(memberships, 2)}
    for a, b in covalent_pairs:
        for first, second in product(by_atom.get(int(a), ()), by_atom.get(int(b), ())):
            if first != second:
                excluded.add((min(first, second), max(first, second)))
    return excluded
