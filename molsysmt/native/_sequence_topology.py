"""Construct the represented group hierarchy without an invented atom domain."""

import numpy as np
import pandas as pd


def from_group_records(records):
    """Build independent canonical tables from already interpreted record groups."""
    from molsysmt.element.group import get_group_type_from_group_name
    from molsysmt.element.group.amino_acid.codes import aa3_to_aa1

    from ._topology_infer import infer_molecule_types_from_topology
    from .topology import Topology

    names = [name for record in records for name in record["groups"]]
    count = len(records)
    topology = Topology(
        n_groups=len(names), n_molecules=count, n_entities=count, n_chains=count
    )
    topology.groups["group_id"] = pd.array(
        [str(i) for i in range(len(names))], dtype="string"
    )
    topology.groups["group_name"] = pd.array(names, dtype="string")
    topology.groups["group_type"] = pd.array(
        [
            "amino acid" if name in aa3_to_aa1 else get_group_type_from_group_name(name)
            for name in names
        ],
        dtype="string",
    )
    topology.groups["molecule_index"] = pd.array(
        np.repeat(np.arange(count), [len(record["groups"]) for record in records]),
        dtype="Int64",
    )
    labels = [record.get("id", str(index)) for index, record in enumerate(records)]
    descriptions = [
        record.get("description", label) for record, label in zip(records, labels)
    ]
    types = (
        infer_molecule_types_from_topology(topology) if names else ["unknown"] * count
    )
    for singular, table in [
        ("molecule", topology.molecules),
        ("entity", topology.entities),
        ("chain", topology.chains),
    ]:
        table[f"{singular}_id"] = pd.array(
            labels if singular == "chain" else [str(i) for i in range(count)],
            dtype="string",
        )
        table[f"{singular}_name"] = pd.array(
            descriptions if singular == "entity" else labels, dtype="string"
        )
        table[f"{singular}_type"] = pd.array(types, dtype="string")
    topology.molecules["entity_index"] = pd.array(range(count), dtype="Int64")
    return topology
