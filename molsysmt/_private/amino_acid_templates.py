"""Select chemical references without using sequence-parent substitutions."""

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from importlib.resources import files

from molsysmt._private.residue_templates import CURATED_MODIFIED_RESIDUES
from molsysmt._private.smonitor import StructuralInconsistencyError


def is_hydrogen(name):
    """Recognize hydrogen names in the bundled peptide/PDB naming variants."""
    return bool(name) and (
        name[0] == "H" or len(name) > 1 and name[0].isdigit() and name[1] == "H"
    )


def family(name, naming_scheme, *, caller, require_context=True):
    """Distinguish supported chemical references from reporting-only parents."""
    from molsysmt._private.name_resolution import _profiles, assessed

    if not isinstance(name, str) or not name:
        return None
    if name in CURATED_MODIFIED_RESIDUES and naming_scheme in (None, "ccd"):
        return "curated_ccd"
    meaning = assessed(
        name, naming_scheme, caller=caller, require_context=require_context
    )
    if meaning is None or meaning.group_type != "amino acid":
        return None
    parents = _profiles()["amber"]["parents"]
    if name in parents:
        if parents[name] == name:
            return "standard"
        if naming_scheme == "amber":
            return "amber_state"
    return None


@lru_cache(maxsize=None)
def _catalogue(name):
    from molsysmt.element.group.amino_acid import get_group_db

    return tuple(get_group_db(name)["topology"])


def _matches_state(variant, fragment):
    """Compare heavy topology and per-parent H counts independently of H labels."""
    atoms = {a["name"]: a for a in fragment["atoms"]}
    heavy = {a for a in variant["atoms"] if not is_hydrogen(a)}
    if heavy != atoms.keys():
        return False
    edges = {frozenset(b["atom_names"]) for b in fragment["bonds"]}
    heavy_edges, counts, hydrogen_degrees = set(), Counter(), Counter()
    for a, b in variant["bonds"]:
        if a in heavy and b in heavy:
            heavy_edges.add(frozenset((a, b)))
        elif is_hydrogen(a) and b in heavy:
            counts[b] += 1
            hydrogen_degrees[a] += 1
        elif is_hydrogen(b) and a in heavy:
            counts[a] += 1
            hydrogen_degrees[b] += 1
        else:
            return False
    return (
        heavy_edges == edges
        and all(counts[a] == record["hydrogen_count"] for a, record in atoms.items())
        and all(hydrogen_degrees[h] == 1 for h in variant["atoms"] if is_hydrogen(h))
    )


@lru_cache(maxsize=None)
def _verified_state_variants(name):
    """Keep independently checked catalogue and Amber construction H layouts."""
    from molsysmt._private.peptide_builder_data import atom_variant
    from molsysmt._private.peptide_chemical_template import _fragments

    library, _ = _fragments()
    fragment = library["residues"][name]
    selected = [v for v in _catalogue(name) if _matches_state(v, fragment)]
    if not selected:
        raise StructuralInconsistencyError(
            reason=f"No bundled atom/bond variant matches the declared Amber {name} state fragment.",
            caller="molsysmt.element.group.amino_acid",
        )
    construction = atom_variant(name)
    if construction is not None:
        if not _matches_state(construction, fragment):
            raise StructuralInconsistencyError(
                reason=f"Bundled construction layout disagrees with the declared Amber {name} state fragment.",
                caller="molsysmt.element.group.amino_acid",
            )
        selected.append(construction)
    return tuple(selected)


def variants(name, naming_scheme, *, caller, require_context=True):
    """Return only supported exact-name variants, or None for unassessed chemistry."""
    kind = family(name, naming_scheme, caller=caller, require_context=require_context)
    if kind == "standard":
        return _catalogue(name)
    if kind == "amber_state":
        return _verified_state_variants(name)
    return None


def choose_variant(candidates, present_names, *, match_hydrogens=True):
    """Match available atom names without falling back after a heavy-atom conflict."""
    if present_names is None:
        return candidates[0]
    heavy = {a for a in present_names if not is_hydrogen(a)}
    hydrogens = {a for a in present_names if is_hydrogen(a)}
    selected, best = None, None
    for candidate in candidates:
        candidate_heavy = {a for a in candidate["atoms"] if not is_hydrogen(a)}
        if not heavy <= candidate_heavy:
            continue
        overlap = (
            len(hydrogens.intersection(candidate["atoms"])) if match_hydrogens else 0
        )
        score = (-overlap, len(candidate_heavy) - len(heavy))
        if best is None or score < best:
            selected, best = candidate, score
    return selected


@lru_cache(maxsize=None)
def _catalogue_reference(name):
    basename = name[0] + ".pkl.gz"
    raw = files("molsysmt.data.databases.amino_acids").joinpath(basename).read_bytes()
    digest = sha256(raw).hexdigest()
    return dict(
        id=f"dataset:molsysmt-amino-acid-catalogue:{digest}",
        type="dataset",
        title="Historical MolSysMT amino-acid atom/bond catalogue",
        url=f"https://github.com/uibcdf/molsysmt/blob/main/molsysmt/data/databases/amino_acids/{basename}",
        roles=["chemical_reference_data"],
    )


def references(name, kind):
    """Return detached reference records without requiring optional tracking."""
    from copy import deepcopy

    from molsysmt._private.residue_templates import load_residue_template

    if kind is None:
        return []
    if kind == "curated_ccd":
        source = load_residue_template(name)["source"]
        items = [
            dict(
                id=f"dataset:ccd-template:{name}:{source['sha256']}",
                type="dataset",
                title=f"CCD-derived exact {name} heavy-atom template",
                url=source["url"],
                roles=["chemical_reference_data"],
            )
        ]
    else:
        items = [dict(_catalogue_reference(name))]
        if kind == "amber_state":
            from molsysmt._private.name_resolution import references
            from molsysmt._private.peptide_chemical_template import _fragments

            items.extend(references("amber", alphabet=False))
            if any("_resource" in v for v in _verified_state_variants(name)):
                from molsysmt._private.peptide_builder_data import reference

                items.append(reference())

            library, _ = _fragments()
            source = library["source"]
            items.append(
                dict(
                    id=f"dataset:meeko-residue-templates:{source['sha256']}",
                    type="dataset",
                    title=source["title"],
                    url=source["url"],
                    version=source["commit"],
                    roles=["chemical_reference_data"],
                )
            )
    return deepcopy(items)


def credit(name, kind, caller):
    """Credit the reference data actually inspected, without claiming an engine."""
    from molsysmt import _ackredit

    with _ackredit.scope(caller) as provider:
        items = references(name, kind)
        _ackredit.credit(provider, items, caller, contextual=True)


def check_external_preparation(
    source, engine, caller, *, selection="all", syntax="MolSysMT"
):
    """Refuse contextual labels until an external naming adapter is implemented.

    Fixed-state preparation does not interpret group labels and bypasses this
    check. Bare standard labels retain the selected engine's existing behavior.
    """
    from molsysmt._private.name_resolution import stored_topology
    from molsysmt._private.smonitor import NotImplementedMethodError
    from molsysmt.basic import convert

    topology = stored_topology(source, caller=caller)
    if topology is None:
        topology = convert(source, to_form="molsysmt.Topology")
    schemes = topology.group_naming_schemes
    from molsysmt._private.name_resolution import _profiles
    from molsysmt._private.variables import is_all
    from molsysmt.basic import select
    from molsysmt.element.group.terminal_capping import group_names as cap_names

    indices = (
        range(topology.n_groups)
        if is_all(selection)
        else select(source, element="group", selection=selection, syntax=syntax)
    )

    contextual = _profiles()["contextual_names"]
    for index in indices:
        name = topology.groups.at[int(index), "group_name"]
        if (
            isinstance(name, str)
            and name in cap_names
            and schemes[index] is not None
            and schemes[index] not in ("amber", "legacy")
        ):
            raise NotImplementedMethodError(
                caller=caller,
                message=f"{engine} preparation has no source-naming adapter for cap label {name!r} under {schemes[index]!r} at group index {index}. No legacy cap meaning is substituted.",
            )
        if isinstance(name, str) and (
            name in contextual
            or name in CURATED_MODIFIED_RESIDUES
            and schemes[index] not in (None, "ccd")
        ):
            family(name, schemes[index], caller=caller)
            raise NotImplementedMethodError(
                caller=caller,
                message=f"{engine} preparation has no source-naming adapter for contextual label {name!r} at group index {index}. Use supported native references or fixed-state preparation from ChemicalStates; no naming convention is translated implicitly.",
            )


def inference_selection(topology, atom_indices="all"):
    """Keep raw readers permissive without inferring chemistry for undeclared labels.

    This only filters missing naming context; it does not claim that references
    exist for all remaining groups. Explicit source edges are never filtered.
    """
    import numpy as np

    from molsysmt._private.name_resolution import _profiles
    from molsysmt._private.variables import is_all
    from molsysmt.native._group_naming import stored

    codes = stored(topology)
    contextual = _profiles()["contextual_names"]
    unresolved = [
        i
        for i, name in enumerate(topology.groups["group_name"])
        if isinstance(name, str)
        and name in contextual
        and (codes is None or codes[i] == 0)
    ]
    if not unresolved:
        return atom_indices
    positions = (
        np.arange(topology.n_atoms, dtype=np.int64)
        if is_all(atom_indices)
        else np.asarray(atom_indices, dtype=np.int64)
    )
    groups = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    return positions[~np.isin(groups[positions], unresolved)]
