"""Reconstruct declared atom-free hierarchy without an atom-requiring builder."""

import pandas as pd

from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
from molsysmt._private.smonitor import StructuralInconsistencyError


def from_records(data):
    from .topology import Topology

    records = {
        name: data.get(name, []) or []
        for name in ("groups", "chains", "molecules", "entities")
    }
    topology = Topology(
        n_groups=len(records["groups"]),
        n_chains=len(records["chains"]),
        n_molecules=len(records["molecules"]),
        n_entities=len(records["entities"]),
    )
    from molsysmt.element.chain.chain_names import _alphabetic_chain_id

    for name, singular in (
        ("groups", "group"),
        ("chains", "chain"),
        ("molecules", "molecule"),
        ("entities", "entity"),
    ):
        table = getattr(topology, name)
        for field in ("id", "name", "type"):
            column = singular + "_" + field
            values = [row.get(column) for row in records[name]]
            if field == "id":
                values = [
                    (_alphabetic_chain_id(index) if singular == "chain" else str(index))
                    if value is None
                    else str(value)
                    for index, value in enumerate(values)
                ]
            table[column] = pd.array(values, dtype="string")
    for group in records["groups"]:
        if group.get("atom_indices", []):
            raise StructuralInconsistencyError(
                reason="An atom-free group cannot reference undefined atoms."
            )
    if data.get("bonds"):
        raise StructuralInconsistencyError(
            reason="An atom-free hierarchy cannot declare atomic bonds."
        )
    for parents, child_table, membership, field in (
        (records["molecules"], topology.groups, "group_indices", "molecule_index"),
        (records["entities"], topology.molecules, "molecule_indices", "entity_index"),
    ):
        assigned = set()
        for parent, record in enumerate(parents):
            indices = flat_axis(
                record.get(membership, []), membership, "TopologyDict conversion"
            )
            if (
                indices is None
                or isinstance(indices, str)
                or any(index >= len(child_table) for index in indices)
                or len(set(indices)) != len(indices)
                or any(int(index) in assigned for index in indices)
            ):
                raise StructuralInconsistencyError(
                    reason="Hierarchy parent records overlap or reference undefined children."
                )
            assigned.update(int(index) for index in indices)
            child_table.loc[indices, field] = parent
    if records["chains"]:
        topology.set_chain_groups(
            [record.get("group_indices", []) for record in records["chains"]]
        )
    return topology
