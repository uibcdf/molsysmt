"""Private stable-topology layer probe for H5MSM 0.5."""

import h5py
import numpy as np
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
    from molsysmt.native._atom_molecules import stored

    stored(topology)
    if getattr(topology, "_chain_group_membership", None) is not None:
        from molsysmt.native._chain_groups import by_chain, pack

        pack(topology, by_chain(topology))
    for name, columns in _TABLES.items():
        if set(getattr(topology, name).columns) != set(columns):
            raise ValueError(f"Topology table {name!r} has a noncanonical schema.")


def write_independent_topology(root, topology, *, compression="gzip"):
    """Write only stable inventory and hierarchy, without covalent records."""
    if "topology" in root:
        raise ValueError("The topology layer already exists.")
    validate_independent_topology(topology)

    group = root.create_group("topology")
    membership = getattr(topology, "_chain_group_membership", None)
    from molsysmt.native._atom_molecules import stored

    atom_molecules = stored(topology)
    if (
        atom_molecules is None
        and topology.n_atoms
        and topology.n_molecules
        and not topology.n_groups
    ):
        # A new unknown declaration must not look like the legacy implicit
        # reference-component encoding when both domains are loaded together.
        atom_molecules = np.full(topology.n_atoms, -1, dtype=np.int64)
    group.attrs["schema_version"] = (
        3 if atom_molecules is not None else 1 if membership is None else 2
    )
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
    if membership is not None:
        from molsysmt.native._chain_groups import by_chain

        by_chain(topology)
        packed = group.create_group("chain_groups")
        packed.create_dataset("offsets", data=membership[0], dtype="i8")
        packed.create_dataset("indices", data=membership[1], dtype="i8")
    if atom_molecules is not None:
        options = {"compression": compression} if compression is not None else {}
        group.create_dataset(
            "atom_molecules", data=atom_molecules, dtype="i8", **options
        )


def read_independent_topology(root):
    """Read an optional stable topology without synthesizing chemistry."""
    if "topology" not in root:
        return None
    group = root["topology"]
    version = group.attrs.get("schema_version")
    if version not in (1, 2, 3):
        raise ValueError("Unsupported H5MSM 0.5 topology layer schema.")
    expected = set(_TABLES) | ({"chain_groups"} if version == 2 else set())
    if version == 3:
        expected |= {"atom_molecules"}
        if "chain_groups" in group:
            expected.add("chain_groups")
    if set(group) != expected:
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
    if version == 2 or version == 3 and "chain_groups" in group:
        packed = group["chain_groups"]
        if set(packed) != {"offsets", "indices"}:
            raise ValueError("Invalid topology chain/group membership datasets.")
        offsets, indices = packed["offsets"][:], packed["indices"][:]
        if (
            offsets.ndim != 1
            or indices.ndim != 1
            or offsets.dtype.kind not in "iu"
            or indices.dtype.kind not in "iu"
            or len(offsets) != topology.n_chains + 1
            or offsets[0] != 0
            or np.any(offsets[1:] < offsets[:-1])
            or offsets[-1] != len(indices)
        ):
            raise ValueError("Invalid topology chain/group membership offsets.")
        try:
            topology.set_chain_groups(
                [indices[offsets[i] : offsets[i + 1]] for i in range(topology.n_chains)]
            )
        except Exception as error:
            raise ValueError("Invalid topology chain/group membership.") from error
    if version == 3:
        from molsysmt.native._atom_molecules import compact, stored

        dataset = group["atom_molecules"]
        if (
            dataset.shape != (topology.n_atoms,)
            or dataset.dtype.kind != "i"
            or dataset.dtype.itemsize != 8
        ):
            raise ValueError(
                "Invalid topology atom/molecule membership shape or dtype."
            )
        values = np.asarray(dataset[:], dtype=np.int64)
        topology._atom_molecule_membership = values
        try:
            stored(topology)
        except Exception as error:
            raise ValueError("Invalid topology atom/molecule membership.") from error
        topology._atom_molecule_membership = compact(values)
    return topology
