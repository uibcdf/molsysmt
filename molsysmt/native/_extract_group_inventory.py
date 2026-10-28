"""Extract represented group hierarchy without inferring absent atomic structure."""

import numpy as np

from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all

from ._chain_groups import by_chain
from ._group_hierarchy import TABLES, members


def extract(topology, indices, element, *, copy_if_all=True):
    if topology.n_atoms:
        raise ValueError("Group-inventory extraction requires zero stored atoms.")
    if is_all(indices):
        return topology.copy() if copy_if_all else topology
    axis = flat_axis(indices, "selection", "group inventory extraction")
    count = len(getattr(topology, TABLES[element]))
    if axis is None or isinstance(axis, str) or np.any(axis >= count):
        raise ArgumentError(
            "selection", message="Invalid hierarchy extraction indices."
        )
    if len(np.unique(axis)) != len(axis):
        raise ArgumentError("selection", message="Extraction indices must be unique.")
    chosen = {element: axis.tolist()}
    context = {}
    for target in TABLES:
        if target != element:
            chosen[target] = sorted(
                {
                    child
                    for index in axis
                    for child in members(
                        topology, element, int(index), target, context=context
                    )
                }
            )
    output = topology.copy()
    for kind, table in TABLES.items():
        setattr(
            output,
            table,
            getattr(topology, table).iloc[chosen[kind]].reset_index(drop=True).copy(),
        )
    for table, field, parent in (
        (output.groups, "molecule_index", "molecule"),
        (output.molecules, "entity_index", "entity"),
    ):
        table[field] = (
            table[field]
            .map({old: new for new, old in enumerate(chosen[parent])})
            .astype("Int64")
        )
    group_map = {old: new for new, old in enumerate(chosen["group"])}
    membership = by_chain(topology)
    output.set_chain_groups(
        [
            [group_map[int(g)] for g in membership[chain] if int(g) in group_map]
            for chain in chosen["chain"]
        ]
    )
    for kind, table in TABLES.items():
        getattr(output, table)[kind + "_id"] = getattr(output, table)[
            kind + "_id"
        ].astype("string")
    return output
