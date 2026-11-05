"""Interpret explicit source labels without selecting or modifying chemistry."""

import json
from functools import lru_cache
from importlib.resources import files
from typing import NamedTuple

from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


class Resolution(NamedTuple):
    parent: str | None
    group_type: str
    profile: str


@lru_cache(maxsize=1)
def _profiles():
    """Read the single bounded offline profile asset only when used."""
    value = json.loads(
        files("molsysmt.data")
        .joinpath("databases/naming_schemes/group_name_profiles.json")
        .read_text()
    )
    if (
        value.get("schema") != "molsysmt.group_name_profiles@1"
        or value.get("version") != 1
    ):
        raise StructuralInconsistencyError(
            reason="Unsupported bundled group naming profiles."
        )
    from molsysmt.element.group.amino_acid.codes import aa3_to_aa1

    contextual = set(value["amber"]["parents"]) - set(aa3_to_aa1)
    contextual.update(
        code
        for code, entry in value["ccd"]["entries"].items()
        if code in aa3_to_aa1 and entry["group_type"] != "amino acid"
    )
    value["contextual_names"] = frozenset(contextual)
    return value


def resolve(name, naming_scheme, *, caller):
    """Return a bounded naming interpretation, keeping parent projection explicit."""
    from molsysmt.element.group.amino_acid.codes import aa3_to_aa1
    from molsysmt.element.group.amino_acid.group_types import name_to_type

    profiles = _profiles()
    if naming_scheme is None:
        # These states need context even where their projected letter agrees.
        if name in profiles["contextual_names"]:
            raise ArgumentError(
                "naming_scheme",
                value=None,
                caller=caller,
                message=f"Group name {name!r} has context-dependent meanings. Set naming_scheme explicitly to 'sequence', 'amber', 'ccd' or 'legacy'; no convention is inferred.",
            )
        if name in aa3_to_aa1:
            return Resolution(name, "amino acid", "sequence")
        entry = profiles["ccd"]["entries"].get(name)
        if entry is not None and entry["parent"] == name_to_type.get(name):
            return Resolution(entry["parent"], entry["group_type"], "ccd")
        raise ArgumentError(
            "naming_scheme",
            value=None,
            caller=caller,
            message=f"No unambiguous naming interpretation is assessed for {name!r}. Supply its supported source naming_scheme explicitly.",
        )
    if naming_scheme == "sequence":
        if name in aa3_to_aa1:
            return Resolution(name, "amino acid", "sequence")
    elif naming_scheme == "amber":
        if name in profiles["amber"]["parents"]:
            return Resolution(profiles["amber"]["parents"][name], "amino acid", "amber")
    elif naming_scheme == "ccd":
        entry = profiles["ccd"]["entries"].get(name)
        if entry is not None:
            return Resolution(entry["parent"], entry["group_type"], "ccd")
    elif naming_scheme == "legacy":
        if name in aa3_to_aa1:
            return Resolution(name, "amino acid", "legacy")
        if name in name_to_type:
            return Resolution(name_to_type[name], "amino acid", "legacy")
    raise ArgumentError(
        "name",
        value=name,
        caller=caller,
        message=f"Group name {name!r} is not supported by the bounded {naming_scheme!r} naming profile. No fallback to another profile is performed.",
    )


def one_letter(name, naming_scheme, *, caller):
    """Project an assessed amino-acid interpretation into the shared alphabet."""
    from molsysmt.element.group.amino_acid.codes import aa3_to_aa1

    result = resolve(name, naming_scheme, caller=caller)
    if result.group_type != "amino acid" or result.parent not in aa3_to_aa1:
        raise ArgumentError(
            "name",
            value=name,
            caller=caller,
            message=f"Group {name!r} under {result.profile!r} has no supported amino-acid one-letter projection. Non-peptide CCD compounds are not unknown sequence symbols.",
        )
    return aa3_to_aa1[result.parent], result.profile


def requires_naming_context(name):
    """Identify the reviewed labels that cannot select their own vocabulary."""
    return isinstance(name, str) and name in _profiles()["contextual_names"]


def assessed(name, naming_scheme, *, caller, require_context=False):
    """Return a reviewed interpretation or no assessment, without legacy fallback.

    Readers preserve ambiguous labels as unknown. Explicit user queries can
    require context instead; neither route infers a convention from a file form.
    """
    if not isinstance(name, str) or not name:
        return None
    from molsysmt.element.group.amino_acid.codes import aa3_to_aa1

    profiles = _profiles()
    if naming_scheme is None:
        if name in profiles["contextual_names"]:
            return resolve(name, None, caller=caller) if require_context else None
        entry = profiles["ccd"]["entries"].get(name)
        if name in aa3_to_aa1 or entry is not None:
            # The default resolver independently checks agreement of reviewed
            # CCD and historical parents; an unassessed compound stays unknown.
            from molsysmt.element.group.amino_acid.group_types import name_to_type

            if name in aa3_to_aa1 or entry["parent"] == name_to_type.get(name):
                return resolve(name, None, caller=caller)
    elif (
        naming_scheme == "sequence"
        and name in aa3_to_aa1
        or naming_scheme == "amber"
        and name in profiles["amber"]["parents"]
        or naming_scheme == "ccd"
        and name in profiles["ccd"]["entries"]
    ):
        return resolve(name, naming_scheme, caller=caller)
    elif naming_scheme == "legacy":
        from molsysmt.element.group.amino_acid.group_types import name_to_type

        if name in aa3_to_aa1 or name in name_to_type:
            return resolve(name, naming_scheme, caller=caller)
    return None


def classify_group_name(group_name, naming_scheme=None, *, require_context=False):
    """Recognize assessed peptide labels before independent non-peptide catalogs."""
    result = assessed(
        group_name,
        naming_scheme,
        caller="molsysmt.element.group.get_group_type_from_group_name",
        require_context=require_context,
    )
    if result is not None:
        return result.group_type
    if not isinstance(group_name, str):
        return "unknown"
    # A potentially peptide/state label cannot fall through to a different
    # catalog merely because its selected naming profile has no assessment.
    from molsysmt.element.group.amino_acid.codes import aa3_to_aa1
    from molsysmt.element.group.amino_acid.group_names import group_names
    from molsysmt.element.group.amino_acid.group_types import name_to_type

    if (
        group_name in aa3_to_aa1
        or group_name in group_names
        or group_name in name_to_type
    ):
        return "unknown"
    from molsysmt.element.group.ion import is_ion
    from molsysmt.element.group.lipid import is_lipid
    from molsysmt.element.group.nucleotide import is_nucleotide
    from molsysmt.element.group.saccharide import is_saccharide
    from molsysmt.element.group.small_molecule import is_small_molecule
    from molsysmt.element.group.terminal_capping import is_terminal_capping
    from molsysmt.element.group.water import is_water

    for predicate, kind in (
        (is_water, "water"),
        (is_ion, "ion"),
        (is_terminal_capping, "terminal capping"),
        (is_nucleotide, "nucleotide"),
        (is_small_molecule, "small molecule"),
        (is_lipid, "lipid"),
        (is_saccharide, "saccharide"),
    ):
        if predicate(group_name):
            return kind
    return "unknown"


def references(profile, *, alphabet=True):
    """Declare only the data and alphabet reached by a successful projection."""
    profiles = _profiles()
    records = [
        dict(
            id="ddbj-amino-acid-code-alphabet",
            type="dataset",
            title="DDBJ codes used in sequence description: amino acids",
            url=profiles["sequence"]["source_url"],
            roles=["reference_data"],
        )
    ]
    if not alphabet and profile != "sequence":
        records.clear()
    if profile == "ccd":
        records.append(
            dict(
                id="rcsb-ccd-group-names-20261104",
                type="dataset",
                title="RCSB CCD component metadata: bounded MolSysMT naming snapshot",
                version=profiles["ccd"]["snapshot_date"],
                url="https://www.wwpdb.org/data/ccd",
                roles=["reference_data"],
            )
        )
    elif profile in {"amber", "legacy"}:
        source = profiles[profile]["source"]
        records.append(
            dict(
                id=f"molsysmt-group-names:{profile}:{source['commit']}",
                type="dataset",
                title="AmberClassic amino12 naming library"
                if profile == "amber"
                else "Historical MDTraj-derived MolSysMT name mapping",
                revision=source["commit"],
                url=source["url"],
                roles=["reference_data"],
            )
        )
    return records


def group_positions(topology, group_indices, *, caller):
    """Check original group positions before indexing or interpreting a label."""
    import numpy as np

    from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
    from molsysmt._private.variables import is_all

    if np.ma.isMaskedArray(group_indices):
        raise ArgumentError("group_indices", value=group_indices, caller=caller)
    positions = (
        np.arange(topology.n_groups, dtype=np.int64)
        if is_all(group_indices)
        else flat_axis(group_indices, "group_indices", caller)
    )
    if (
        positions is None
        or isinstance(positions, str)
        or np.any(positions >= topology.n_groups)
    ):
        raise ArgumentError("group_indices", value=group_indices, caller=caller)
    return positions


def check_source_scheme(topology, positions, from_naming_scheme, *, caller):
    """Refuse contradictions on selected groups without changing declarations."""
    import numpy as np

    from molsysmt.native._group_naming import NAMES, stored

    codes = stored(topology)
    if from_naming_scheme is not None and codes is not None:
        requested = NAMES.index(from_naming_scheme)
        conflicts = positions[(codes[positions] != 0) & (codes[positions] != requested)]
        if len(conflicts):
            raise ArgumentError(
                "from_naming_scheme",
                value=from_naming_scheme,
                caller=caller,
                message=f"Source naming scheme contradicts stored declarations for selected group indices {np.unique(conflicts).tolist()}. Select compatible groups or explicitly edit their declarations first.",
            )
    return codes


def native_sequence(topology, group_indices, *, caller, from_naming_scheme=None):
    """Project native group positions and credit reached profiles once per query."""
    from molsysmt.native._group_naming import NAMES

    positions = group_positions(topology, group_indices, caller=caller)
    codes = check_source_scheme(topology, positions, from_naming_scheme, caller=caller)
    names = topology.groups["group_name"].to_numpy(dtype=object)[positions]
    kinds = topology.groups["group_type"].to_numpy(dtype=object)[positions]
    schemes = (
        from_naming_scheme
        if from_naming_scheme is not None
        else None
        if codes is None
        else NAMES[codes[index]]
        for index in positions
    )
    return project_sequence(names, kinds, positions, schemes, caller=caller)[0]


def project_sequence(names, kinds, positions, schemes, *, caller, with_indices=False):
    """Resolve letters and optional source positions under one attribution batch."""
    from molsysmt import _ackredit

    letters, used_profiles = [], {}
    source_indices = [] if with_indices else None
    for name, kind, index, scheme in zip(names, kinds, positions, schemes, strict=True):
        if not isinstance(kind, str) or kind != "amino acid":
            if not isinstance(kind, str) or kind == "unknown":
                interpretation = assessed(
                    name, scheme, caller=caller, require_context=True
                )
                if interpretation is None or interpretation.group_type != "amino acid":
                    continue
            else:
                continue
        if not isinstance(name, str) or not name:
            raise ArgumentError(
                "name",
                value=name,
                caller=caller,
                message=f"Selected group {int(index)} has no amino-acid name.",
            )
        letter, profile = one_letter(name.upper(), scheme, caller=caller)
        letters.append(letter)
        if source_indices is not None:
            source_indices.append(int(index))
        used_profiles[profile] = None
    if used_profiles:
        items = {
            item["id"]: item
            for profile in used_profiles
            for item in references(profile)
        }
        with _ackredit.scope(caller) as provider:
            _ackredit.credit(provider, list(items.values()), caller, contextual=True)
    return "".join(letters), source_indices


def stored_topology(source, *, caller):
    """Read a known naming container without decoding unrelated molecular domains."""
    from molsysmt.native import MolSys, MolSysDict, Topology, TopologyDict

    known = True
    if isinstance(source, Topology):
        topology = source
    elif isinstance(source, MolSys):
        topology = source.topology
    elif isinstance(source, (TopologyDict, MolSysDict)):
        from molsysmt.form._native_dict import decode_topology

        data = (
            source.data
            if isinstance(source, TopologyDict)
            else source.data.get("topology")
        )
        topology = None if data is None else decode_topology(data)
    elif isinstance(source, (list, tuple)):
        from molsysmt.basic import where_is_attribute

        owner, _ = where_is_attribute(source, "group_name")
        return stored_topology(owner, caller=caller)
    else:
        from molsysmt._private.h5msm import modular_h5msm_axes

        if modular_h5msm_axes(source) is not None:
            from molsysmt.h5msm import read_layers

            topology = read_layers(source, layers=["topology"])["topology"]
        else:
            known, topology = False, None
    if known and topology is None:
        raise ArgumentError(
            "molecular_system",
            caller=caller,
            message="Sequence projection requires a topology with group names.",
        )
    return topology
