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


def references(profile):
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
    from molsysmt import _ackredit
    from molsysmt.native._group_naming import NAMES

    positions = group_positions(topology, group_indices, caller=caller)
    codes = check_source_scheme(topology, positions, from_naming_scheme, caller=caller)
    names = topology.groups["group_name"].to_numpy(dtype=object)[positions]
    kinds = topology.groups["group_type"].to_numpy(dtype=object)[positions]
    letters, used_profiles = [], {}
    for name, kind, index in zip(names, kinds, positions, strict=True):
        if not isinstance(kind, str) or kind != "amino acid":
            continue
        if not isinstance(name, str) or not name:
            raise ArgumentError(
                "name",
                value=name,
                caller=caller,
                message=f"Selected group {int(index)} has no amino-acid name.",
            )
        scheme = (
            from_naming_scheme
            if from_naming_scheme is not None
            else None
            if codes is None
            else NAMES[codes[index]]
        )
        letter, profile = one_letter(name.upper(), scheme, caller=caller)
        letters.append(letter)
        used_profiles[profile] = None
    if used_profiles:
        items = {
            item["id"]: item
            for profile in used_profiles
            for item in references(profile)
        }
        with _ackredit.scope(caller) as provider:
            _ackredit.credit(provider, list(items.values()), caller, contextual=True)
    return "".join(letters)
