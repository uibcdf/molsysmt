"""Compact declared chain/group membership, independent of atomic realization."""

import numpy as np
import pandas as pd

from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


def pack(topology, memberships):
    if memberships is None:
        return None
    if len(memberships) != topology.n_chains:
        raise ArgumentError(
            "chain_groups", message="Provide one ordered group list per native chain."
        )
    offsets = [0]
    pieces = []
    for members in memberships:
        values = flat_axis(members, "chain_groups", "Topology.set_chain_groups")
        if (
            values is None
            or isinstance(values, str)
            or np.any(values >= topology.n_groups)
        ):
            raise ArgumentError(
                "chain_groups",
                message="Chain groups require valid source group indices.",
            )
        if len(np.unique(values)) != len(values):
            raise ArgumentError(
                "chain_groups", message="A group may occur only once within a chain."
            )
        pieces.append(values)
        offsets.append(offsets[-1] + len(values))
    offsets = np.asarray(offsets, dtype=np.int64)
    groups = np.concatenate(pieces) if pieces else np.empty(0, dtype=np.int64)
    # Existing atom membership is evidence, never silently replaced by a declaration.
    if topology.n_atoms:
        declared = {i: set(piece.tolist()) for i, piece in enumerate(pieces)}
        for group, chain in topology.atoms[["group_index", "chain_index"]].itertuples(
            index=False, name=None
        ):
            if (
                not pd.isna(group)
                and not pd.isna(chain)
                and int(group) not in declared.get(int(chain), set())
            ):
                raise StructuralInconsistencyError(
                    reason="Declared chain groups conflict with stored atom membership."
                )
    offsets.flags.writeable = groups.flags.writeable = False
    return offsets, groups


def by_chain(topology):
    declared = getattr(topology, "_chain_group_membership", None)
    if declared is not None:
        offsets, indices = declared
        if len(offsets) != topology.n_chains + 1 or np.any(
            indices >= topology.n_groups
        ):
            raise StructuralInconsistencyError(
                reason="Chain/group inventory changed; explicitly remap or reset its membership."
            )
        return [indices[offsets[i] : offsets[i + 1]] for i in range(topology.n_chains)]
    result = [set() for _ in range(topology.n_chains)]
    for group, chain in topology.atoms[["group_index", "chain_index"]].itertuples(
        index=False, name=None
    ):
        if not pd.isna(group) and not pd.isna(chain) and 0 <= int(chain) < len(result):
            result[int(chain)].add(int(group))
    return [np.asarray(sorted(groups), dtype=np.int64) for groups in result]


def by_group(topology):
    result = [[] for _ in range(topology.n_groups)]
    for chain, groups in enumerate(by_chain(topology)):
        for group in groups:
            result[int(group)].append(chain)
    return result


def uses_declared_hierarchy(topology):
    return (
        topology.n_atoms == 0
        or getattr(topology, "_chain_group_membership", None) is not None
    )
