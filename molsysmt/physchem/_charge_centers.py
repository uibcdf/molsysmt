"""Interpreting formal charges on bounded covalent motifs."""

import numpy as np

from molsysmt.topology._functional_group_candidates import (
    terminal_oxygen_and_guanidine_candidates,
)


def formal_charge_centers(elements, charges, pairs, bond_orders):
    """Group specified motifs and directly connected charged atoms deterministically."""

    parent = np.arange(len(elements), dtype=np.int64)

    def root(atom):
        while parent[atom] != atom:
            parent[atom] = parent[parent[atom]]
            atom = parent[atom]
        return int(atom)

    def join(first, second):
        first, second = root(first), root(second)
        if first != second:
            parent[max(first, second)] = min(first, second)

    motifs = list(
        terminal_oxygen_and_guanidine_candidates(elements, pairs, bond_orders)
    )
    for _, members, _ in motifs:
        for atom in members[1:]:
            join(members[0], atom)
    for first, second in pairs:
        if charges[first] != 0 and charges[second] != 0:
            join(first, second)

    members_by_root = {}
    geometry_by_root = {}
    kinds_by_root = {}
    motif_atoms = set()
    for kind, members, geometry in motifs:
        key = root(members[0])
        members_by_root.setdefault(key, set()).update(members.tolist())
        geometry_by_root.setdefault(key, set()).update(geometry.tolist())
        kinds_by_root.setdefault(key, set()).add(kind)
        motif_atoms.update(members.tolist())
    for atom in np.flatnonzero(charges):
        key = root(atom)
        members_by_root.setdefault(key, set()).add(int(atom))
        if atom not in motif_atoms:
            geometry_by_root.setdefault(key, set()).add(int(atom))

    centers = []
    for key, members in members_by_root.items():
        members = sorted(members)
        charge = int(np.sum(charges[members]))
        if charge == 0:
            continue
        kinds = kinds_by_root.get(key, set())
        member_elements = elements[members]
        member_charges = charges[members]
        if (
            kinds == {"carboxyl"}
            and len(members) == 3
            and member_charges[member_elements == "C"].tolist() == [0]
            and sorted(member_charges[member_elements == "O"].tolist()) == [-1, 0]
        ):
            kind = "carboxylate"
        elif (
            kinds == {"guanidine"}
            and len(members) == 4
            and member_charges[member_elements == "C"].tolist() == [0]
            and sorted(member_charges[member_elements == "N"].tolist()) == [0, 0, 1]
        ):
            kind = "guanidinium"
        elif len(members) == 1:
            kind = "formal_charge_atom"
        else:
            kind = "formal_charge_cluster"
        centers.append((members, sorted(geometry_by_root[key]), charge, kind))
    centers.sort(key=lambda center: center[0])
    return centers


def pack_membership(groups):
    """Pack atom-index groups into int64 values and offsets, including empty input."""

    offsets = np.zeros(len(groups) + 1, dtype=np.int64)
    np.cumsum([len(group) for group in groups], out=offsets[1:])
    return np.asarray(
        [atom for group in groups for atom in group], dtype=np.int64
    ), offsets
