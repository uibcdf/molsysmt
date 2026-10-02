"""Private stable-topology layer probe for H5MSM 0.5."""

import h5py
import pandas as pd

from molsysmt.native.chemical_states_dict import _decode_series, _encode_series
from molsysmt.native.topology import Topology

_TABLES = {
    "atoms": (
        "atom_id",
        "atom_name",
        "atom_type",
        "isotope",
        "group_index",
        "chain_index",
    ),
    "groups": ("group_id", "group_name", "group_type", "molecule_index"),
    "molecules": ("molecule_id", "molecule_name", "molecule_type", "entity_index"),
    "entities": ("entity_id", "entity_name", "entity_type"),
    "chains": ("chain_id", "chain_name", "chain_type"),
}


def validate_independent_topology(topology):
    """Validate the stable topology tables before creating a file."""
    if not isinstance(topology, Topology):
        raise TypeError("The topology layer requires native Topology.")
    for name, columns in _TABLES.items():
        if set(getattr(topology, name).columns) != set(columns):
            raise ValueError(f"Topology table {name!r} has a noncanonical schema.")


def write_independent_topology(root, topology, *, compression="gzip"):
    """Write only stable inventory and hierarchy, without covalent records."""
    if "topology" in root:
        raise ValueError("The topology layer already exists.")
    validate_independent_topology(topology)

    group = root.create_group("topology")
    group.attrs["schema_version"] = 1
    for name, columns in _TABLES.items():
        table = getattr(topology, name)
        table_group = group.create_group(name)
        table_group.attrs["n_rows"] = len(table)
        for column in columns:
            payload = _encode_series(table[column])
            column_group = table_group.create_group(column)
            column_group.attrs["dtype"] = payload["dtype"]
            values = payload["values"]
            options = {"compression": compression} if compression is not None else {}
            if values.dtype.kind in "USO":
                column_group.create_dataset(
                    "values",
                    data=values.astype(object),
                    dtype=h5py.string_dtype(),
                    **options,
                )
            else:
                column_group.create_dataset("values", data=values, **options)
            column_group.create_dataset(
                "null_mask", data=payload["null_mask"], **options
            )


def read_independent_topology(root):
    """Read an optional stable topology without synthesizing chemistry."""
    if "topology" not in root:
        return None
    group = root["topology"]
    if group.attrs.get("schema_version") != 1:
        raise ValueError("Unsupported H5MSM 0.5 topology layer schema.")
    if set(group) != set(_TABLES):
        raise ValueError("The topology layer has missing or unknown tables.")

    tables = {}
    for name, columns in _TABLES.items():
        table_group = group[name]
        if set(table_group) != set(columns):
            raise ValueError(f"Topology table {name!r} has missing or unknown columns.")
        n_rows = int(table_group.attrs["n_rows"])
        if n_rows < 0:
            raise ValueError(f"Topology table {name!r} has an invalid row count.")
        table = pd.DataFrame(index=range(n_rows))
        for column in columns:
            column_group = table_group[column]
            if set(column_group) != {"values", "null_mask"}:
                raise ValueError(
                    f"Topology column {name}/{column} has an invalid schema."
                )
            dataset = column_group["values"]
            values = dataset.asstr()[:] if dataset.dtype.kind in "OSU" else dataset[:]
            payload = {
                "dtype": column_group.attrs["dtype"],
                "values": values,
                "null_mask": column_group["null_mask"][:],
            }
            series = _decode_series(payload)
            if len(series) != n_rows:
                raise ValueError(
                    f"Topology column {name}/{column} has the wrong length."
                )
            table[column] = series
        tables[name] = table

    topology = Topology(
        n_atoms=len(tables["atoms"]),
        n_groups=len(tables["groups"]),
        n_molecules=len(tables["molecules"]),
        n_entities=len(tables["entities"]),
        n_chains=len(tables["chains"]),
        skip_digestion=True,
    )
    for name, table in tables.items():
        target = getattr(topology, name)
        for column in table:
            target[column] = table[column]
    topology._coerce_id_columns_to_string()
    topology._clear_chemical_states()
    return topology
