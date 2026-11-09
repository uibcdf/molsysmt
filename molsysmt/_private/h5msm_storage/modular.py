"""Private development-root composition, reusing the existing domain codecs."""

from datetime import datetime, timezone
from numbers import Integral
from pathlib import Path

import h5py
import pandas as pd

from molsysmt.form._h5msm05_associations import (
    _axis_sizes,
    _axis_sizes_from_file,
    normalize_associations,
    read_associations,
    write_associations,
)
from molsysmt.form._h5msm05_structures import (
    _prepared_series,
    read_independent_structures,
    write_independent_structures,
)
from molsysmt.form._h5msm05_topology import (
    read_independent_topology,
    validate_independent_topology,
    write_independent_topology,
)
from molsysmt.form._h5msm_chemical_states import (
    read_independent_chemical_states,
    write_independent_chemical_states,
)
from molsysmt.interactions._hdf5_collection import (
    read_named_analyses,
    write_named_analyses,
)
from molsysmt.native._mechanics_presence import has_stored_mechanics
from molsysmt.native._transport import (
    _validate_chemical_states_extensions,
    _validate_molsys_extensions,
    _validate_structures_extensions,
    _validate_topology_extensions,
)

from ..files_and_directories import atomic_new_file
from .mechanics import (
    _atom_count,
    _prepare_mechanics,
    _write_prepared_mechanics,
    read_mechanics,
)

_DOMAINS = (
    "topology",
    "chemical_states",
    "structures",
    "molecular_mechanics",
    "interactions",
)
_LAYERS = frozenset((*_DOMAINS, "associations"))
_ROOT_ATTRIBUTES = {"type", "version", "creator", "creator_version", "created_at"}
_DEVELOPMENT_VERSION = "0.6"


def _text(value):
    return value.decode() if isinstance(value, bytes) else value


def _header(root):
    version = _text(root.attrs.get("version"))
    if _text(root.attrs.get("type")) != "h5msm" or version not in {
        "0.5",
        _DEVELOPMENT_VERSION,
    }:
        raise ValueError("Unsupported H5MSM modular root version.")
    if version == _DEVELOPMENT_VERSION:
        if set(root) - _LAYERS or set(root.attrs) != _ROOT_ATTRIBUTES:
            raise ValueError("Unsupported development-root fields or metadata.")
        if any(
            not isinstance(_text(root.attrs[name]), str) for name in _ROOT_ATTRIBUTES
        ):
            raise ValueError("H5MSM root metadata must contain explicit text values.")
    return version


def _sizes(payload, mechanics_n_atoms=None):
    sizes = _axis_sizes(
        payload.get("topology"),
        payload.get("chemical_states"),
        payload.get("structures"),
        payload.get("interactions"),
    )
    if payload.get("molecular_mechanics") is not None:
        sizes[("molecular_mechanics", None, "atom")] = _atom_count(mechanics_n_atoms)
    return sizes


def _declared_sizes(root):
    sizes = _axis_sizes_from_file(root)
    if "molecular_mechanics" in root:
        sizes[("molecular_mechanics", None, "atom")] = _atom_count(
            root["molecular_mechanics"].attrs["n_atoms"]
        )
    return sizes


def _preflight(payload, mechanics_n_atoms):
    from molsysmt.interactions.result import Interactions
    from molsysmt.native import ChemicalStates, Structures, Topology

    for name, cls in (
        ("topology", Topology),
        ("chemical_states", ChemicalStates),
        ("structures", Structures),
    ):
        if payload[name] is not None and not isinstance(payload[name], cls):
            raise TypeError(f"The {name} layer requires native {cls.__name__}.")
    if payload["topology"] is not None:
        _validate_topology_extensions(payload["topology"])
        validate_independent_topology(payload["topology"])
        for name in ("atoms", "groups", "molecules", "entities", "chains"):
            if getattr(payload["topology"], name).attrs:
                raise ValueError("Untyped topology table metadata cannot be discarded.")
    if payload["chemical_states"] is not None:
        states = payload["chemical_states"]
        _validate_chemical_states_extensions(states)
        reference = states._reference_index
        if reference is not None and (
            isinstance(reference, bool)
            or not isinstance(reference, Integral)
            or not 0 <= reference < states.n_chemical_states
        ):
            raise ValueError("Chemical-state reference index is outside its inventory.")
        for state in states._states:
            state._validate_atom_domain(states.n_atoms)
            if any(
                table.attrs
                for table in (
                    state.atom_attributes,
                    state.bonds,
                    state.components,
                    state.component_indices,
                )
            ):
                raise ValueError("Untyped chemical table metadata cannot be discarded.")
    if payload["structures"] is not None:
        _validate_structures_extensions(payload["structures"])
        _prepared_series(payload["structures"])
    if payload["interactions"] is not None:
        analyses = payload["interactions"]
        if type(analyses) is not dict:
            raise TypeError("Named analyses require a dictionary.")
        for name, result in analyses.items():
            if not isinstance(name, str) or not name:
                raise ValueError("Interaction names must be nonempty text.")
            if not isinstance(result, Interactions) or not result._is_full:
                raise ValueError("Named analyses require full Interactions results.")
    if payload["molecular_mechanics"] is None:
        if mechanics_n_atoms is not None:
            raise ValueError("A mechanical atom count requires a mechanics layer.")
        return None
    return _prepare_mechanics(payload["molecular_mechanics"], mechanics_n_atoms)


def write_modular_file(
    filename,
    *,
    topology=None,
    chemical_states=None,
    structures=None,
    molecular_mechanics=None,
    mechanics_n_atoms=None,
    interactions=None,
    associations=None,
):
    """Stage a private development file and publish only after successful close."""
    payload = dict(
        topology=topology,
        chemical_states=chemical_states,
        structures=structures,
        molecular_mechanics=molecular_mechanics,
        interactions=interactions,
    )
    if all(value is None for value in payload.values()):
        raise ValueError("A modular file requires at least one declared domain.")
    prepared_mechanics = _preflight(payload, mechanics_n_atoms)
    links = normalize_associations(
        associations, _sizes(payload, mechanics_n_atoms), layers=_DOMAINS
    )
    from molsysmt import __version__

    with atomic_new_file(filename) as staged:
        with h5py.File(staged, "w") as file:
            file.attrs.update(
                type="h5msm",
                version=_DEVELOPMENT_VERSION,
                creator="MolSysMT",
                creator_version=__version__,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            if prepared_mechanics is not None:
                _write_prepared_mechanics(
                    file, prepared_mechanics, n_atoms=mechanics_n_atoms
                )
            if topology is not None:
                write_independent_topology(file, topology)
            if chemical_states is not None:
                write_independent_chemical_states(file, chemical_states)
            if structures is not None:
                write_independent_structures(file, structures)
            if interactions is not None:
                write_named_analyses(file.create_group("interactions"), interactions)
            write_associations(file, links)


def read_modular_file(filename, *, layers=None, analysis_names=None):
    """Read requested resident layers, retaining independently declared maps."""
    requested = (
        _LAYERS
        if layers is None
        else {layers}
        if isinstance(layers, str)
        else set(layers)
    )
    if requested - _LAYERS:
        raise ValueError("Unsupported modular layer requested.")
    if analysis_names is not None and "interactions" not in requested:
        raise ValueError("analysis_names requires the interactions layer.")
    with h5py.File(Path(filename), "r") as file:
        version = _header(file)
        if version != "0.5":
            result = {}
            for name, reader in (
                ("topology", read_independent_topology),
                ("chemical_states", read_independent_chemical_states),
                ("structures", read_independent_structures),
                ("molecular_mechanics", read_mechanics),
            ):
                if name in requested:
                    result[name] = reader(file)
            if "interactions" in requested:
                result["interactions"] = (
                    read_named_analyses(file["interactions"], names=analysis_names)
                    if "interactions" in file
                    else None
                )
                if analysis_names is not None and result["interactions"] is None:
                    raise KeyError("The file has no interaction analyses.")
            if "associations" in requested:
                result["associations"] = read_associations(
                    file, _declared_sizes(file), layers=_DOMAINS
                )
            return result
    from molsysmt.form._h5msm05_modular import read_modular_file as read_05

    result = read_05(
        filename,
        layers=requested - {"molecular_mechanics"},
        analysis_names=analysis_names,
    )
    if "molecular_mechanics" in requested:
        result["molecular_mechanics"] = None
    return result


def _nodes(sizes, axis):
    rank = {name: index for index, name in enumerate(_DOMAINS)}
    return sorted(
        [(name, label) for name, label, kind in sizes if kind == axis],
        key=lambda item: (rank[item[0]], item[1] or ""),
    )


def read_axis_sizes(filename):
    """Read declared per-domain cardinalities without materializing payloads."""
    with h5py.File(filename, "r") as file:
        _header(file)
        sizes = _declared_sizes(file)
        if any(value < 0 for value in sizes.values()):
            raise ValueError("Invalid modular layer axis cardinality.")
        return sizes


def _identity(axis, source, target):
    return dict(
        axis=axis,
        source=source[0],
        source_name=source[1],
        target=target[0],
        target_name=target[1],
        indices="identity",
    )


def _native_links(payload, sizes, state_indices):
    links = []
    for axis in ("atom", "structure"):
        nodes = _nodes(sizes, axis)
        links.extend(_identity(axis, source, nodes[0]) for source in nodes[1:])
    if state_indices is not None:
        if payload["structures"] is None or payload["chemical_states"] is None:
            raise ValueError("Structure-state assignments require both domains.")
        if str(getattr(state_indices, "dtype", None)) != "Int64":
            raise ValueError(
                "Native structure-state assignments require nullable integer storage."
            )
        links.append(
            dict(
                axis="structure_state",
                source="structures",
                source_name=None,
                target="chemical_states",
                target_name=None,
                indices=[
                    -1 if pd.isna(value) else int(value) for value in state_indices
                ],
            )
        )
    return links


def _require_shared_axes(links, sizes, *, axes=("atom", "structure")):
    """Require identity-connected axes; equal cardinalities provide no evidence."""
    for axis in axes:
        nodes = _nodes(sizes, axis)
        neighbors = {node: set() for node in nodes}
        for link in links:
            if link["axis"] != axis:
                continue
            if not isinstance(link["indices"], str) or link["indices"] != "identity":
                raise ValueError(
                    "MolSys requires identity associations; read independent layers to align explicit maps."
                )
            source, target = (
                (link["source"], link["source_name"]),
                (link["target"], link["target_name"]),
            )
            neighbors[source].add(target)
            neighbors[target].add(source)
        if nodes:
            pending, visited = [nodes[0]], set()
            while pending:
                node = pending.pop()
                if node not in visited:
                    visited.add(node)
                    pending.extend(neighbors[node] - visited)
            if len(visited) != len(nodes):
                raise ValueError(
                    "MolSys requires declared identity associations for shared axes."
                )


def write_molsys_file(filename, molsys):
    """Store represented native domains without discarding mechanical evidence."""
    from molsysmt.native import MolSys

    if not isinstance(molsys, MolSys):
        raise TypeError("A native MolSys is required.")
    _validate_molsys_extensions(molsys)
    payload = dict(
        topology=molsys.topology,
        chemical_states=molsys.chemical_states,
        structures=molsys.structures,
        interactions=dict(molsys.interactions) or None,
        molecular_mechanics=molsys.molecular_mechanics
        if has_stored_mechanics(molsys.molecular_mechanics)
        else None,
    )
    count = (
        molsys._get_n_atoms() if payload["molecular_mechanics"] is not None else None
    )
    sizes = _sizes(payload, count)
    links = _native_links(payload, sizes, molsys._structure_chemical_state_indices)
    # This also rejects inconsistent native atom/structure axis cardinalities.
    normalize_associations(links, sizes, layers=_DOMAINS)
    write_modular_file(filename, **payload, mechanics_n_atoms=count, associations=links)


def read_molsys_file(filename):
    """Assemble native ownership only for explicitly aligned stored domains."""
    with h5py.File(filename, "r") as file:
        version = _header(file)
    if version == "0.5":
        from molsysmt.form._h5msm05_modular import read_molsys_file as read_05

        return read_05(filename)
    payload = read_modular_file(filename)
    mechanics = payload["molecular_mechanics"]
    if mechanics is not None and not has_stored_mechanics(mechanics):
        raise ValueError(
            "An explicitly empty mechanics layer has no native presence marker; read its independent layer."
        )
    analyses = payload["interactions"]
    if analyses is not None and not analyses:
        raise ValueError(
            "An empty analysis collection has no native presence marker; read its independent layer."
        )
    if (
        all(
            payload[name] is None
            for name in ("topology", "chemical_states", "structures")
        )
        and not analyses
    ):
        raise ValueError(
            "A mechanics-only file requires independent layer reading; MolSys has no standalone mechanics axis."
        )
    with h5py.File(filename, "r") as file:
        sizes = _declared_sizes(file)
    links = payload["associations"] or []
    _require_shared_axes(links, sizes)
    if payload["molecular_mechanics"] is not None and all(
        node[0] == "molecular_mechanics" for node in _nodes(sizes, "atom")
    ):
        raise ValueError(
            "Mechanics requires a compatible native atom domain; read independent layers."
        )
    state_links = [link for link in links if link["axis"] == "structure_state"]
    if len(state_links) > 1 or any(
        link["source"] != "structures" or link["target"] != "chemical_states"
        for link in state_links
    ):
        raise ValueError(
            "MolSys requires a single Structures-to-ChemicalStates association."
        )
    from molsysmt.native import MolSys

    result = MolSys._from_partial_domains(
        topology=payload["topology"],
        chemical_states=payload["chemical_states"],
        structures=payload["structures"],
        interactions=analyses
        if all(
            payload[name] is None
            for name in ("topology", "chemical_states", "structures")
        )
        else None,
    )
    if state_links:
        indices = state_links[0]["indices"]
        if isinstance(indices, str):
            indices = range(result.structures.n_structures)
        result._set_structure_chemical_state_indices(
            [pd.NA if value < 0 else int(value) for value in indices]
        )
    result.interactions = analyses or {}
    if payload["molecular_mechanics"] is not None:
        result.molecular_mechanics = payload["molecular_mechanics"]
    return result
