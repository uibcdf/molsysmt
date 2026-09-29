"""Private four-layer H5MSM 0.5 file probe with explicit axis links."""

from pathlib import Path

import h5py
import numpy as np

from molsysmt.interactions._hdf5_collection import (
    read_named_analyses,
    write_named_analyses,
)

from ._h5msm05_associations import (
    _axis_sizes,
    _axis_sizes_from_file,
    normalize_associations,
    read_associations,
    write_associations,
)
from ._h5msm05_structures import (
    _prepared_series,
    append_independent_structures,
    read_independent_structures,
    write_independent_structures,
)
from ._h5msm05_topology import (
    read_independent_topology,
    validate_independent_topology,
    write_independent_topology,
)
from ._h5msm_chemical_states import (
    read_independent_chemical_states,
    write_independent_chemical_states,
)


def write_modular_file(filename, *, topology=None, chemical_states=None,
                       structures=None, interactions=None, associations=None):
    """Write optional independent domains after validating declared axis links."""
    from molsysmt.interactions.result import Interactions
    from molsysmt.native import ChemicalStates, Structures, Topology

    if topology is not None and not isinstance(topology, Topology):
        raise TypeError("topology must be native Topology or None.")
    if chemical_states is not None and not isinstance(chemical_states, ChemicalStates):
        raise TypeError("chemical_states must be native ChemicalStates or None.")
    if structures is not None and not isinstance(structures, Structures):
        raise TypeError("structures must be native Structures or None.")
    if interactions is not None:
        interactions = dict(interactions)
        for name, result in interactions.items():
            if not isinstance(name, str) or not name:
                raise ValueError("Interaction analysis names must be nonempty strings.")
            if not isinstance(result, Interactions) or not result._is_full:
                raise TypeError("Interaction analyses must contain full Interactions results.")

    if topology is not None:
        validate_independent_topology(topology)
    if structures is not None:
        _prepared_series(structures)

    sizes = _axis_sizes(topology, chemical_states, structures, interactions)
    links = normalize_associations(associations, sizes)
    with h5py.File(Path(filename), "x") as file:
        file.attrs["type"] = "h5msm"
        file.attrs["version"] = "0.5"
        file.attrs["creator"] = "MolSysMT"
        if topology is not None:
            write_independent_topology(file, topology)
        if chemical_states is not None:
            write_independent_chemical_states(file, chemical_states)
        if structures is not None:
            write_independent_structures(file, structures)
        if interactions is not None:
            write_named_analyses(file.create_group("interactions"), interactions)
        write_associations(file, links)


def _prepare_structure_state_append(file, links, indices, count, sizes):
    """Validate one existing per-frame state map before any dataset grows."""
    matching = [
        (position, link) for position, link in enumerate(links)
        if link["axis"] == "structure_state"
    ]
    if not matching:
        if indices is not None:
            raise ValueError("No structure-to-state association exists to extend.")
        return None
    if len(matching) != 1:
        raise ValueError("Appending requires a single structure-to-state association.")
    position, link = matching[0]
    if link["source"] != "structures" or link["target"] != "chemical_states":
        raise ValueError("Appending cannot extend this structure-axis association.")
    if count == 0 and indices is None:
        return None
    if indices is None:
        raise ValueError("structure_state_indices are required for appended structures.")
    incoming = np.asarray(indices)
    if incoming.size == 0:
        incoming = np.asarray(indices, dtype=np.int64)
    if incoming.ndim != 1 or incoming.shape != (count,) or incoming.dtype.kind not in "iu":
        raise ValueError("structure_state_indices must match the appended structure axis.")
    if incoming.dtype.kind == "u" and np.any(incoming > np.iinfo(np.int64).max):
        raise ValueError("structure_state_indices exceed the supported index range.")
    incoming = incoming.astype(np.int64, copy=False)
    n_states = sizes[("chemical_states", None, "state")]
    if np.any(incoming < -1) or np.any(incoming >= n_states):
        raise ValueError("structure_state_indices contain an index outside the state axis.")

    child = file[f"associations/{position}"]
    old_count = sizes[("structures", None, "structure")]
    mapping = child.attrs["mapping"]
    if mapping == "identity":
        old_indices = np.arange(old_count, dtype=np.int64)
    else:
        dataset = child["indices"]
        if dataset.dtype != np.dtype("int64") or dataset.maxshape[0] is not None:
            raise ValueError("The stored structure-to-state association is not appendable.")
        old_indices = dataset[:]
    joined = np.concatenate((old_indices, incoming))
    updated_sizes = dict(sizes)
    updated_sizes[("structures", None, "structure")] = old_count + count
    updated_links = list(links)
    updated_links[position] = {**link, "indices": joined}
    normalize_associations(updated_links, updated_sizes)
    return child, mapping, old_count, incoming, joined


def append_modular_structures(
    filename, structures, *, structure_state_indices=None, block_size=256
):
    """Append complete frames to a topology-free file with optional state links."""
    from molsysmt.native import Structures

    if not isinstance(structures, Structures):
        raise TypeError("The structures layer requires native Structures.")
    with h5py.File(Path(filename), "r+") as file:
        if file.attrs.get("type") != "h5msm" or file.attrs.get("version") != "0.5":
            raise ValueError("Expected an H5MSM 0.5 modular file.")
        if "structures" not in file or set(file) - {
            "structures", "chemical_states", "associations"
        }:
            raise ValueError("Appending requires a topology-free file without interactions.")
        sizes = _axis_sizes_from_file(file)
        links = read_associations(file, sizes) or []
        if any(link["axis"] == "structure" for link in links):
            raise ValueError("Appending cannot extend a stored structure-axis association.")
        state_update = _prepare_structure_state_append(
            file, links, structure_state_indices, structures.n_structures, sizes
        )
        append_independent_structures(file, structures, block_size=block_size)
        if state_update is not None:
            child, mapping, old_count, incoming, joined = state_update
            if mapping == "identity":
                if not np.array_equal(joined, np.arange(len(joined))):
                    child.create_dataset(
                        "indices", data=joined, maxshape=(None,), compression="gzip"
                    )
                    child.attrs["mapping"] = "explicit"
            else:
                dataset = child["indices"]
                dataset.resize(old_count + len(incoming), axis=0)
                dataset[old_count:] = incoming


def read_modular_file(filename, *, layers=None, analysis_names=None):
    """Read selected optional domains and validate requested associations."""
    allowed = {
        "topology", "chemical_states", "structures", "interactions", "associations"
    }
    requested = (
        allowed if layers is None
        else {layers} if isinstance(layers, str)
        else set(layers)
    )
    if requested - allowed:
        raise ValueError("Unknown H5MSM 0.5 layer requested.")
    if analysis_names is not None and "interactions" not in requested:
        raise ValueError("analysis_names requires the interactions layer.")
    with h5py.File(Path(filename), "r") as file:
        if file.attrs.get("type") != "h5msm" or file.attrs.get("version") != "0.5":
            raise ValueError("Expected an H5MSM 0.5 modular file.")
        if set(file) - allowed:
            raise ValueError("H5MSM 0.5 file contains an unknown root layer.")
        result = {}
        if "topology" in requested:
            result["topology"] = read_independent_topology(file)
        if "chemical_states" in requested:
            result["chemical_states"] = read_independent_chemical_states(file)
        if "structures" in requested:
            result["structures"] = read_independent_structures(file)
        if "interactions" in requested:
            result["interactions"] = (
                read_named_analyses(file["interactions"], names=analysis_names)
                if "interactions" in file else None
            )
            if analysis_names is not None and result["interactions"] is None:
                raise KeyError("The file has no interaction analyses.")
        if "associations" in requested:
            result["associations"] = read_associations(file, _axis_sizes_from_file(file))
        return result


def _identity_link(axis, source, target, *, source_name=None):
    return {
        "axis": axis, "source": source, "target": target,
        "source_name": source_name, "target_name": None,
        "indices": "identity",
    }


def _link_key(link):
    return (
        link["axis"], link["source"], link["source_name"],
        link["target"], link["target_name"],
    )


def write_complete_molsys_file(filename, molsys):
    """Probe lossless four-domain persistence for a complete native MolSys."""
    import pandas as pd

    from molsysmt.native import MolSys

    if not isinstance(molsys, MolSys):
        raise TypeError("A complete H5MSM 0.5 MolSys probe requires native MolSys.")
    mechanics = molsys.molecular_mechanics.to_dict()
    if any(value is not None for value in mechanics.values()):
        raise ValueError("H5MSM 0.5 probe cannot encode molecular mechanics yet.")

    analyses = dict(molsys.interactions)
    sizes = _axis_sizes(
        molsys.topology, molsys.chemical_states, molsys.structures, analyses
    )
    links = [_identity_link("atom", "chemical_states", "topology")]
    if ("structures", None, "atom") in sizes:
        links.append(_identity_link("atom", "structures", "topology"))
    for name in sorted(analyses):
        links.append(_identity_link("atom", "interactions", "topology", source_name=name))
        links.append(_identity_link("structure", "interactions", "structures", source_name=name))
    association = molsys._structure_chemical_state_indices
    if association is not None:
        links.append({
            "axis": "structure_state", "source": "structures",
            "target": "chemical_states", "source_name": None,
            "target_name": None,
            "indices": [
                -1 if pd.isna(value) else int(value) for value in association
            ],
        })
    normalize_associations(links, sizes)
    write_modular_file(
        filename, topology=molsys.topology,
        chemical_states=molsys.chemical_states,
        structures=molsys.structures,
        interactions=analyses or None,
        associations=links,
    )


def read_complete_molsys_file(filename):
    """Rebuild one complete MolSys only when all required axes align."""
    import pandas as pd

    from molsysmt.native import MolSys

    payload = read_modular_file(filename)
    topology = payload["topology"]
    states = payload["chemical_states"]
    structures = payload["structures"]
    if topology is None or states is None or structures is None:
        raise ValueError("A complete MolSys requires topology, chemical states, and structures.")
    links = payload["associations"]
    if links is None:
        raise ValueError("A complete MolSys requires explicit atom-axis associations.")
    by_key = {_link_key(link): link for link in links}
    required = [_identity_link("atom", "chemical_states", "topology")]
    sizes = _axis_sizes(topology, states, structures, payload["interactions"])
    if ("structures", None, "atom") in sizes:
        required.append(_identity_link("atom", "structures", "topology"))
    for name in sorted(payload["interactions"] or {}):
        required.append(_identity_link("atom", "interactions", "topology", source_name=name))
        required.append(_identity_link("structure", "interactions", "structures", source_name=name))
    state_key = ("structure_state", "structures", None, "chemical_states", None)
    allowed_keys = {_link_key(link) for link in required} | {state_key}
    if set(by_key) - allowed_keys:
        raise ValueError("MolSys cannot represent an extra H5MSM axis association.")
    for link in required:
        observed = by_key.get(_link_key(link))
        if observed is None or not (
            isinstance(observed["indices"], str)
            and observed["indices"] == "identity"
        ):
            raise ValueError("MolSys requires declared identity links for shared axes.")

    result = MolSys()
    result.topology = topology
    result.chemical_states = states
    result.structures = structures
    if state_key in by_key:
        indices = by_key[state_key]["indices"]
        if isinstance(indices, str):
            indices = range(structures.n_structures)
        result._set_structure_chemical_state_indices(
            [pd.NA if value < 0 else int(value) for value in indices]
        )
    result.interactions = payload["interactions"] or {}
    return result


def read_state_only_molsys_file(filename):
    """Probe native ownership of a state-only 0.5 payload without a topology."""

    from molsysmt.native import MolSys

    payload = read_modular_file(filename)
    if payload["chemical_states"] is None:
        raise ValueError("A state-only MolSys requires chemical states.")
    if any(payload[name] is not None for name in (
        "topology", "structures", "interactions", "associations"
    )):
        raise ValueError("A state-only MolSys cannot contain other H5MSM layers.")
    return MolSys._from_partial_domains(
        chemical_states=payload["chemical_states"]
    )


def write_topology_free_molsys_file(filename, molsys):
    """Probe persistence of native chemistry and structures without topology."""
    import pandas as pd

    from molsysmt.native import MolSys

    if not isinstance(molsys, MolSys) or molsys.topology is not None:
        raise TypeError("A topology-free H5MSM probe requires a partial native MolSys.")
    mechanics = molsys.molecular_mechanics.to_dict()
    if any(value is not None for value in mechanics.values()):
        raise ValueError("H5MSM 0.5 probe cannot encode molecular mechanics yet.")
    structures = molsys.structures
    analyses = dict(molsys.interactions)

    sizes = _axis_sizes(None, molsys.chemical_states, structures, analyses)
    links = []
    if ("structures", None, "atom") in sizes:
        links.append(_identity_link("atom", "structures", "chemical_states"))
    for name in sorted(analyses):
        links.append(_identity_link(
            "atom", "interactions", "chemical_states", source_name=name
        ))
        if structures is not None:
            links.append(_identity_link(
                "structure", "interactions", "structures", source_name=name
            ))
    association = molsys._structure_chemical_state_indices
    if association is not None:
        if structures is None:
            raise ValueError("Structure-to-state associations require structures.")
        links.append({
            "axis": "structure_state", "source": "structures",
            "target": "chemical_states", "source_name": None,
            "target_name": None,
            "indices": [-1 if pd.isna(value) else int(value) for value in association],
        })
    write_modular_file(
        filename, chemical_states=molsys.chemical_states,
        structures=structures, interactions=analyses or None,
        associations=links or None,
    )


def read_topology_free_molsys_file(filename):
    """Rebuild a partial MolSys only when every shared axis is identified."""
    import pandas as pd

    from molsysmt.native import MolSys

    payload = read_modular_file(filename)
    if payload["topology"] is not None or payload["chemical_states"] is None:
        raise ValueError("A topology-free MolSys requires states and no topology.")
    structures = payload["structures"]
    analyses = payload["interactions"]
    if analyses is not None and not analyses:
        raise ValueError("MolSys cannot represent a present-empty interaction layer yet.")

    links = payload["associations"] or []
    by_key = {_link_key(link): link for link in links}
    sizes = _axis_sizes(None, payload["chemical_states"], structures, analyses)
    required = []
    if ("structures", None, "atom") in sizes:
        required.append(_identity_link("atom", "structures", "chemical_states"))
    for name in sorted(analyses or {}):
        required.append(_identity_link(
            "atom", "interactions", "chemical_states", source_name=name
        ))
        if structures is not None:
            required.append(_identity_link(
                "structure", "interactions", "structures", source_name=name
            ))
    state_key = ("structure_state", "structures", None, "chemical_states", None)
    allowed_keys = {_link_key(link) for link in required}
    if structures is not None:
        allowed_keys.add(state_key)
    if set(by_key) - allowed_keys:
        raise ValueError("MolSys cannot represent an extra H5MSM axis association.")
    for link in required:
        observed = by_key.get(_link_key(link))
        if observed is None or not (
            isinstance(observed["indices"], str)
            and observed["indices"] == "identity"
        ):
            raise ValueError("MolSys requires declared identity links for shared axes.")

    result = MolSys._from_partial_domains(
        chemical_states=payload["chemical_states"], structures=structures,
        interactions=analyses or {},
    )
    if state_key in by_key:
        indices = by_key[state_key]["indices"]
        if isinstance(indices, str):
            indices = range(structures.n_structures)
        result._set_structure_chemical_state_indices(
            [pd.NA if value < 0 else int(value) for value in indices]
        )
    return result


def write_no_chemical_states_molsys_file(filename, molsys):
    """Probe native persistence when chemical states are genuinely absent."""

    from molsysmt.native import MolSys

    if not isinstance(molsys, MolSys) or molsys.chemical_states is not None:
        raise TypeError("This H5MSM probe requires a MolSys without chemical states.")
    topology = molsys.topology
    structures = molsys.structures
    if topology is None and structures is None:
        raise ValueError("A molecular payload needs topology or structures.")
    if topology is not None and topology._chemical_states_domain.n_chemical_states:
        raise ValueError("The topology contains chemistry absent from MolSys.")
    if molsys._structure_chemical_state_indices is not None:
        raise ValueError("Structure-to-state assignments require chemical states.")
    if any(value is not None for value in molsys.molecular_mechanics.to_dict().values()):
        raise ValueError("H5MSM 0.5 probe cannot encode molecular mechanics yet.")

    analyses = dict(molsys.interactions)
    sizes = _axis_sizes(topology, None, structures, analyses)
    links = []
    if (("topology", None, "atom") in sizes
            and ("structures", None, "atom") in sizes):
        links.append(_identity_link("atom", "structures", "topology"))
    atom_target = "topology" if topology is not None else "structures"
    for name in sorted(analyses):
        links.append(_identity_link(
            "atom", "interactions", atom_target, source_name=name
        ))
        if structures is not None:
            links.append(_identity_link(
                "structure", "interactions", "structures", source_name=name
            ))
    write_modular_file(
        filename, topology=topology, structures=structures,
        interactions=analyses or None,
        associations=links or None,
    )


def read_no_chemical_states_molsys_file(filename):
    """Rebuild absent chemistry without fabricating an empty state layer."""

    from molsysmt.native import MolSys

    payload = read_modular_file(filename)
    topology = payload["topology"]
    structures = payload["structures"]
    if payload["chemical_states"] is not None:
        raise ValueError("This reader requires absent chemical states.")
    analyses = payload["interactions"]
    if analyses is not None and not analyses:
        raise ValueError("MolSys cannot represent a present-empty interaction layer yet.")
    if topology is None and structures is None:
        raise ValueError("A molecular payload needs topology or structures.")
    sizes = _axis_sizes(topology, None, structures, analyses)
    required = []
    if (("topology", None, "atom") in sizes
            and ("structures", None, "atom") in sizes):
        required.append(_identity_link("atom", "structures", "topology"))
    atom_target = "topology" if topology is not None else "structures"
    for name in sorted(analyses or {}):
        required.append(_identity_link(
            "atom", "interactions", atom_target, source_name=name
        ))
        if structures is not None:
            required.append(_identity_link(
                "structure", "interactions", "structures", source_name=name
            ))
    links = payload["associations"] or []
    by_key = {_link_key(link): link for link in links}
    if set(by_key) - {_link_key(link) for link in required}:
        raise ValueError("MolSys cannot represent an extra H5MSM axis association.")
    for link in required:
        observed = by_key.get(_link_key(link))
        if observed is None or not (
            isinstance(observed["indices"], str)
            and observed["indices"] == "identity"
        ):
            raise ValueError("MolSys requires declared identity links for shared axes.")
    return MolSys._from_partial_domains(
        topology=topology, structures=structures, chemical_states=None,
        interactions=analyses or {},
    )


def write_topology_chemistry_molsys_file(filename, molsys):
    """Probe a topology and chemical states with no structures layer."""

    from molsysmt.native import MolSys

    if (not isinstance(molsys, MolSys) or molsys.topology is None
            or molsys.chemical_states is None or molsys.structures is not None):
        raise TypeError("This H5MSM probe requires topology and chemistry only.")
    if molsys.topology._chemical_states_domain is not molsys.chemical_states:
        raise ValueError("Topology and MolSys disagree on the chemical-state authority.")
    if molsys.interactions:
        raise ValueError("This H5MSM probe cannot encode interaction analyses yet.")
    if any(value is not None for value in molsys.molecular_mechanics.to_dict().values()):
        raise ValueError("H5MSM 0.5 probe cannot encode molecular mechanics yet.")
    write_modular_file(
        filename, topology=molsys.topology,
        chemical_states=molsys.chemical_states,
        associations=[_identity_link("atom", "chemical_states", "topology")],
    )


def read_topology_chemistry_molsys_file(filename):
    """Rebuild native topology and chemistry only for one declared atom axis."""

    from molsysmt.native import MolSys

    payload = read_modular_file(filename)
    if (payload["topology"] is None or payload["chemical_states"] is None
            or payload["structures"] is not None or payload["interactions"] is not None):
        raise ValueError("This reader requires topology and chemistry only.")
    expected = _identity_link("atom", "chemical_states", "topology")
    links = payload["associations"] or []
    if len(links) != 1 or _link_key(links[0]) != _link_key(expected) or not (
        isinstance(links[0]["indices"], str)
        and links[0]["indices"] == "identity"
    ):
        raise ValueError("MolSys requires one declared identity atom-axis link.")
    return MolSys._from_partial_domains(
        topology=payload["topology"],
        chemical_states=payload["chemical_states"],
    )


def write_molsys_file(filename, molsys):
    """Write a native MolSys through the supported private 0.5 domain routes."""
    from molsysmt.native import MolSys

    if not isinstance(molsys, MolSys):
        raise TypeError("H5MSM 0.5 requires a native MolSys.")
    if (molsys.topology is None and molsys.chemical_states is None
            and molsys.structures is None):
        if not molsys.interactions:
            raise ValueError("An interaction-only MolSys needs a named analysis.")
        if any(value is not None for value in molsys.molecular_mechanics.to_dict().values()):
            raise ValueError("H5MSM 0.5 cannot encode molecular mechanics yet.")
        return write_modular_file(filename, interactions=dict(molsys.interactions))
    if molsys.chemical_states is None:
        return write_no_chemical_states_molsys_file(filename, molsys)
    if molsys.topology is None:
        return write_topology_free_molsys_file(filename, molsys)
    if molsys.structures is None:
        return write_topology_chemistry_molsys_file(filename, molsys)
    return write_complete_molsys_file(filename, molsys)


def read_molsys_file(filename):
    """Read a native MolSys after inspecting only 0.5 root-layer presence."""
    with h5py.File(Path(filename), "r") as file:
        if file.attrs.get("type") != "h5msm" or file.attrs.get("version") != "0.5":
            raise ValueError("Expected an H5MSM 0.5 modular file.")
        allowed = {
            "topology", "chemical_states", "structures", "interactions", "associations"
        }
        if set(file) - allowed:
            raise ValueError("H5MSM 0.5 file contains an unknown root layer.")
        has_topology = "topology" in file
        has_chemistry = "chemical_states" in file
        has_structures = "structures" in file
        has_interactions = "interactions" in file
    if has_interactions and not (has_topology or has_chemistry or has_structures):
        payload = read_modular_file(filename)
        analyses = payload["interactions"]
        if not analyses:
            raise ValueError(
                "A present-empty interaction layer has no declared atom or structure "
                "index domain; use molsysmt.h5msm.read_layers(filename, "
                "layers='interactions')."
            )
        for link in payload["associations"] or []:
            if not (
                link["axis"] in {"atom", "structure"}
                and link["source"] == "interactions"
                and link["target"] == "interactions"
                and isinstance(link["indices"], str)
                and link["indices"] == "identity"
            ):
                raise ValueError(
                    "An interaction-only MolSys requires identity links between "
                    "named analyses."
                )
        from molsysmt.native import MolSys

        return MolSys._from_partial_domains(interactions=analyses)
    if not has_chemistry:
        return read_no_chemical_states_molsys_file(filename)
    if not has_topology:
        if not has_structures and not has_interactions:
            return read_state_only_molsys_file(filename)
        return read_topology_free_molsys_file(filename)
    if not has_structures:
        return read_topology_chemistry_molsys_file(filename)
    return read_complete_molsys_file(filename)


def migrate_to_05(source_filename, output_filename, *, source_version=None):
    """Translate a legacy H5MSM file through native domain ownership."""
    source = Path(source_filename)
    target = Path(output_filename)
    if source.resolve() == target.resolve():
        raise ValueError("Migration requires distinct source and output filenames.")
    with h5py.File(source, "r") as file:
        version = file.attrs.get("version")
        if isinstance(version, bytes):
            version = version.decode()
        if (file.attrs.get("type") != "h5msm" or version not in {"0.3", "0.4"}
                or (source_version is not None and version != source_version)):
            expected = source_version or "0.3 or 0.4"
            raise ValueError(f"Migration requires an H5MSM {expected} source file.")
        if "topology" not in file or "structures" not in file:
            raise ValueError("The legacy source lacks its topology or structures scaffold.")
        if int(file["topology"].attrs.get("n_atoms", 0)) == 0:
            raise ValueError("A zero-atom legacy scaffold has ambiguous layer presence.")

    from molsysmt.basic import convert

    molsys = convert(str(source), to_form="molsysmt.MolSys")
    write_molsys_file(target, molsys)
    with h5py.File(target, "r+") as file:
        file.attrs["migrated_from_version"] = version
    return target


def migrate_04_to_05(source_filename, output_filename):
    """Translate a complete 0.4 file through the legacy-specific helper."""
    return migrate_to_05(source_filename, output_filename, source_version="0.4")
