"""Versioned dictionary transport for explicitly independent native domains."""

import numpy as np
import pandas as pd

from ._serialization import decode_typed_tree, encode_typed_tree, normalize_scalar

TABLES = {
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


def _reject_extensions(source, allowed):
    """Refuse native payloads this wire schema cannot preserve explicitly."""
    from molsysmt.native._copy import _slots

    if set(vars(source)) - set(allowed) - {"_molsys_owner_ref"} or _slots(
        source, exclude=("_molsys_owner_ref",), qualified=True
    ):
        raise ValueError(
            f"Unsupported {type(source).__name__} extension payload in dictionary export."
        )


def _version(data, kind):
    if not isinstance(data, dict):
        raise ValueError("A native dictionary payload must be a mapping.")
    version = data.get("version", "0.1")
    if version not in {"0.1", "0.2"}:
        raise ValueError(f"Unsupported {kind} dictionary version {version!r}.")
    if version == "0.2" and (
        data.get("format") != "molsysmt" or data.get("kind") != kind
    ):
        raise ValueError(f"Invalid {kind} dictionary identity.")
    return version


def encode_topology(topology):
    """Emit canonical stable rows, including nullable positional memberships."""
    from molsysmt.native import TopologyDict
    from molsysmt.native._atom_molecules import stored
    from molsysmt.native._chain_groups import by_chain

    _reject_extensions(
        topology,
        {
            *TABLES,
            "_atom_molecule_membership",
            "_chain_group_membership",
            "_atoms_dirty",
            "_groups_dirty",
            "_molecules_dirty",
            "_entities_dirty",
            "_chains_dirty",
        },
    )
    data = {"format": "molsysmt", "kind": "topology", "version": "0.2", "metadata": {}}
    for name, columns in TABLES.items():
        table = getattr(topology, name)
        if set(table.columns) != set(columns) or table.attrs:
            raise ValueError(
                "Topology dictionary export requires canonical stable tables without untyped extensions."
            )
        data[name] = [
            {column: normalize_scalar(row[column]) for column in columns}
            for _, row in table.iterrows()
        ]
    membership = stored(topology)
    if membership is not None:
        data["atom_molecules"] = [
            None if value < 0 else int(value) for value in membership
        ]
    if topology._chain_group_membership is not None:
        data["chain_groups"] = [values.tolist() for values in by_chain(topology)]
    return TopologyDict(data=data)


def _position(value, count, label):
    if value is None:
        return None
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, np.integer))
        or not 0 <= value < count
    ):
        raise ValueError(f"Invalid {label} positional reference.")
    return int(value)


def decode_topology(data):
    """Build inventory directly, without allocating or reading chemical states."""
    from molsysmt.native import Topology

    version = _version(data, "topology")
    if version == "0.2":
        required = {"format", "kind", "version", "metadata", *TABLES}
        if (
            not required <= set(data)
            or set(data) - required - {"chain_groups", "atom_molecules"}
            or data["metadata"] != {}
        ):
            raise ValueError("Unsupported TopologyDict 0.2 fields or metadata.")
    rows = {name: data.get(name, []) for name in TABLES}
    if any(
        not isinstance(value, list) or any(not isinstance(row, dict) for row in value)
        for value in rows.values()
    ):
        raise ValueError("Topology tables must be ordered record lists.")
    if version == "0.2" and any(
        set(row) != set(TABLES[name])
        for name, records in rows.items()
        for row in records
    ):
        raise ValueError("Unsupported TopologyDict 0.2 row fields.")
    topology = Topology(
        n_atoms=len(rows["atoms"]),
        n_groups=len(rows["groups"]),
        n_molecules=len(rows["molecules"]),
        n_entities=len(rows["entities"]),
        n_chains=len(rows["chains"]),
        skip_digestion=True,
    )
    for name, columns in TABLES.items():
        table = getattr(topology, name)
        for column in columns:
            values = [row.get(column) for row in rows[name]]
            if column.endswith("_id"):
                values = [None if value is None else str(value) for value in values]
            table[column] = pd.array(values, dtype=table[column].dtype)
    if version == "0.1":
        for owner, child, list_key, column in (
            ("groups", "atoms", "atom_indices", "group_index"),
            ("molecules", "groups", "group_indices", "molecule_index"),
            ("entities", "molecules", "molecule_indices", "entity_index"),
        ):
            assigned = set()
            for index, record in enumerate(rows[owner]):
                values = record.get(list_key, [])
                if not isinstance(values, list):
                    raise ValueError("Legacy membership must be an index list.")
                for member in values:
                    member = _position(member, len(rows[child]), child)
                    if member is None or member in assigned:
                        raise ValueError("Legacy single-owner memberships overlap.")
                    assigned.add(member)
                    getattr(topology, child).loc[member, column] = index
        chains = [record.get("group_indices", []) for record in rows["chains"]]
        if any(chains):
            topology.set_chain_groups(chains, skip_digestion=True)
            for atom, group in enumerate(topology.atoms["group_index"]):
                candidates = [
                    i
                    for i, groups in enumerate(chains)
                    if pd.notna(group) and int(group) in groups
                ]
                if len(candidates) == 1:
                    topology.atoms.loc[atom, "chain_index"] = candidates[0]
    for name, column, target in (
        ("atoms", "group_index", "groups"),
        ("atoms", "chain_index", "chains"),
        ("groups", "molecule_index", "molecules"),
        ("molecules", "entity_index", "entities"),
    ):
        for value in getattr(topology, name)[column]:
            _position(None if pd.isna(value) else value, len(rows[target]), column)
    if "chain_groups" in data:
        topology.set_chain_groups(data["chain_groups"], skip_digestion=True)
    if "atom_molecules" in data:
        topology.set_atom_molecules(data["atom_molecules"], skip_digestion=True)
    topology._coerce_id_columns_to_string()
    return topology


_UNITS = {
    "coordinates": "nm",
    "box": "nm",
    "velocities": "nm/ps",
    "time": "ps",
    "time_step": "ps",
    "b_factor": "nm**2",
    "temperature": "K",
    "potential_energy": "kJ/mol",
    "kinetic_energy": "kJ/mol",
    "translations": "nm",
}


def _structure_quantity(path):
    if (
        not isinstance(path, list)
        or not path
        or any(type(key) not in {str, int} for key in path)
    ):
        raise ValueError("Invalid structural quantity path.")
    name = path[-1]
    if name not in _UNITS:
        raise ValueError("Quantity is outside the declared structural fields.")
    return "molsysmt.Structures/" + "/".join(map(str, path)), _UNITS[name]


def _label_arrays(value, path=()):
    """Represent label-only object arrays as primitive lists, never object bytes."""
    if isinstance(value, np.ndarray) and value.dtype.kind == "O":
        if not path or path[-1] not in {"structure_id", "atom_id", "location_id"}:
            raise ValueError(
                "Only schema-declared label fields admit object arrays as primitive lists."
            )
        return value.tolist()
    if isinstance(value, dict):
        return {
            key: _label_arrays(child, path + (key,)) for key, child in value.items()
        }
    if isinstance(value, list):
        return [
            _label_arrays(child, path + (index,)) for index, child in enumerate(value)
        ]
    return value


def encode_structures(structures):
    from molsysmt.form.molsysmt_Structures.to_molsysmt_StructuresDict import (
        to_molsysmt_StructuresDict,
    )

    _reject_extensions(
        structures,
        {
            "_coordinates",
            "_box",
            "_time",
            "_time_step",
            "_velocities",
            "_b_factor",
            "_occupancy",
            "_temperature",
            "_potential_energy",
            "_kinetic_energy",
            "constant_box",
            "constant_time_step",
            "constant_id_step",
            "id_step",
            "structure_id",
            "alternate_location",
            "bioassembly",
        },
    )
    series = to_molsysmt_StructuresDict(structures, skip_digestion=True)
    alternate = series.get("alternate_location")
    if alternate is not None:
        from collections.abc import Mapping

        if any(not isinstance(mapping, Mapping) for mapping in alternate):
            raise ValueError(
                "MolSysDict alternate locations require sparse atom-to-sites mappings."
            )
        series["alternate_location"] = [
            [
                {"atom_index": int(atom), "sites": sites}
                for atom, sites in mapping.items()
            ]
            for mapping in alternate
        ]
    series["bioassembly"] = structures.bioassembly
    metadata = {
        name: getattr(structures, name)
        for name in (
            "constant_box",
            "constant_time_step",
            "constant_id_step",
            "time_step",
            "id_step",
        )
    }
    return encode_typed_tree(
        _label_arrays({"series": series, "metadata": metadata}),
        quantity_field=_structure_quantity,
    )


def decode_structures(payload):
    from molsysmt.form.molsysmt_StructuresDict.to_molsysmt_Structures import (
        to_molsysmt_Structures,
    )

    data = decode_typed_tree(payload, quantity_field=_structure_quantity)
    if not isinstance(data, dict) or set(data) != {"series", "metadata"}:
        raise ValueError("Invalid structural dictionary domain.")
    series = data["series"]
    if not isinstance(series, dict) or set(series) - {
        *_UNITS,
        "structure_id",
        "occupancy",
        "alternate_location",
        "bioassembly",
    }:
        raise ValueError("Unsupported structural series fields.")
    alternate = series.get("alternate_location")
    if alternate is not None:
        converted = []
        for records in alternate:
            mapping = {}
            for entry in records:
                atom = entry["atom_index"]
                if type(atom) is not int or atom < 0 or atom in mapping:
                    raise ValueError("Invalid or repeated alternate-site atom index.")
                mapping[atom] = entry["sites"]
            converted.append(mapping)
        series["alternate_location"] = converted
    assembly = series.pop("bioassembly", None)
    structures = to_molsysmt_Structures(series, skip_digestion=True)
    structures.bioassembly = assembly
    allowed = {
        "constant_box",
        "constant_time_step",
        "constant_id_step",
        "time_step",
        "id_step",
    }
    if set(data["metadata"]) != allowed:
        raise ValueError("Unsupported structural metadata fields.")
    for name, value in data["metadata"].items():
        setattr(structures, name, value)
    return structures


def encode_molsys(molsys):
    """Encode independent optional domains and explicit associations as schema 0.2."""
    from molsysmt.native import MolSysDict
    from molsysmt.native.chemical_states_dict import (
        _encode_chemical_states,
        _encode_series,
    )
    from molsysmt.native.interactions_dict import _encode_interactions

    _reject_extensions(
        molsys,
        {
            "_topology",
            "_chemical_states_domain",
            "_structures",
            "molecular_mechanics",
            "_structure_chemical_state_indices",
            "_interactions",
        },
    )
    if molsys.chemical_states is not None:
        _reject_extensions(
            molsys.chemical_states, {"_n_atoms", "_states", "_reference_index"}
        )
        for state in molsys.chemical_states._states:
            _reject_extensions(
                state,
                {
                    "state_id",
                    "atom_attributes",
                    "component_indices",
                    "bonds",
                    "components",
                    "_connectivity_completeness",
                    "_component_completeness",
                    "_component_evidence",
                    "_provenance_index",
                    "_preparation_history",
                },
            )
    if molsys.molecular_mechanics is not None and any(
        value is not None for value in molsys.molecular_mechanics.to_dict().values()
    ):
        raise ValueError(
            "MolSysDict 0.2 does not persist MolecularMechanics; omit it explicitly before transport."
        )
    association = molsys._structure_chemical_state_indices
    return MolSysDict(
        {
            "format": "molsysmt",
            "kind": "molsys",
            "version": "0.2",
            "metadata": {},
            "topology": None
            if molsys.topology is None
            else encode_topology(molsys.topology).data,
            "chemical_states": None
            if molsys.chemical_states is None
            else encode_typed_tree(
                _encode_chemical_states(molsys.chemical_states).data
            ),
            "structures": None
            if molsys.structures is None
            else encode_structures(molsys.structures),
            "structure_chemical_state_indices": None
            if association is None
            else encode_typed_tree(
                _encode_series(pd.Series(association, dtype="Int64"))
            ),
            "interactions": {
                name: encode_typed_tree(_encode_interactions(result).data)
                for name, result in molsys.interactions.items()
            },
        }
    )


def decode_molsys(data):
    """Validate domain transports before publishing their aligned native assembly."""
    from molsysmt.native import ChemicalStatesDict, InteractionsDict, MolSys
    from molsysmt.native.chemical_states_dict import (
        _decode_chemical_states,
        _decode_series,
    )
    from molsysmt.native.interactions_dict import _decode_interactions

    if _version(data, "molsys") != "0.2":
        raise ValueError("Legacy dictionaries use the explicit legacy reader.")
    required = {
        "format",
        "kind",
        "version",
        "metadata",
        "topology",
        "chemical_states",
        "structures",
        "structure_chemical_state_indices",
        "interactions",
    }
    if (
        set(data) != required
        or not isinstance(data["interactions"], dict)
        or data["metadata"] != {}
    ):
        raise ValueError("Invalid MolSysDict 0.2 domains.")
    topology = None if data["topology"] is None else decode_topology(data["topology"])
    states = (
        None
        if data["chemical_states"] is None
        else _decode_chemical_states(
            ChemicalStatesDict(decode_typed_tree(data["chemical_states"]))
        )
    )
    structures = (
        None if data["structures"] is None else decode_structures(data["structures"])
    )
    analyses = {
        name: _decode_interactions(InteractionsDict(decode_typed_tree(value)))
        for name, value in data["interactions"].items()
    }
    result = MolSys._from_partial_domains(
        topology=topology,
        chemical_states=states,
        structures=structures,
        interactions=analyses
        if data["structure_chemical_state_indices"] is None
        else None,
    )
    if data["structure_chemical_state_indices"] is not None:
        association = _decode_series(
            decode_typed_tree(data["structure_chemical_state_indices"])
        )
        result._set_structure_chemical_state_indices(association.array)
    result.interactions = analyses
    return result
