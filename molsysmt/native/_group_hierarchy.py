"""Project represented hierarchy directly, without an atomic intermediary."""

import numpy as np
import pandas as pd

from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all

from ._chain_groups import by_chain, by_group

TABLES = {
    "group": "groups",
    "molecule": "molecules",
    "entity": "entities",
    "chain": "chains",
}
GROUP_TYPES = {
    "amino_acids": "amino acid",
    "nucleotides": "nucleotide",
    "waters": "water",
    "ions": "ion",
    "saccharides": "saccharide",
}
MOLECULE_TYPES = {
    "proteins": "protein",
    "peptides": "peptide",
    "small_molecules": "small molecule",
    "dnas": "dna",
    "rnas": "rna",
    "lipids": "lipid",
    "polysaccharides": "polysaccharide",
}


def _clean(value):
    return None if pd.isna(value) else value


def _unique(values):
    return sorted({int(value) for value in values if not pd.isna(value)})


def _children(parents, count):
    valid = np.flatnonzero((parents >= 0) & (parents < count))
    order = valid[np.argsort(parents[valid], kind="stable")]
    offsets = np.concatenate(
        ([0], np.cumsum(np.bincount(parents[valid], minlength=count)))
    )
    return offsets, order


def _lookup(index, packed):
    offsets, children = packed
    return children[offsets[index] : offsets[index + 1]]


def members(topology, source, index, target, *, context=None):
    if source == target:
        return [index]
    context = {} if context is None else context
    if "gm" not in context:
        context["gm"] = topology.groups["molecule_index"].to_numpy(
            dtype=np.int64, na_value=-1
        )
        context["me"] = topology.molecules["entity_index"].to_numpy(
            dtype=np.int64, na_value=-1
        )
    gm, me = context["gm"], context["me"]
    if source == "group":
        groups = [index]
    elif source == "molecule":
        if "molecule_groups" not in context:
            context["molecule_groups"] = _children(gm, topology.n_molecules)
        groups = _lookup(index, context["molecule_groups"])
    elif source == "entity":
        if "entity_molecules" not in context:
            context["entity_molecules"] = _children(me, topology.n_entities)
        mols = _lookup(index, context["entity_molecules"])
        if target == "molecule":
            return mols.tolist()
        groups = [
            group
            for molecule in mols
            for group in members(
                topology, "molecule", int(molecule), "group", context=context
            )
        ]
    else:
        if "chains" not in context:
            context["chains"] = by_chain(topology)
        groups = context["chains"][index]
    if target == "group":
        return [int(group) for group in groups]
    if target == "chain":
        if "inverse" not in context:
            context["inverse"] = by_group(topology)
        return _unique(
            chain for group in groups for chain in context["inverse"][int(group)]
        )
    if target == "molecule":
        return sorted({int(gm[int(group)]) for group in groups if gm[int(group)] >= 0})
    mols = members(topology, source, index, "molecule", context=context)
    return sorted({int(me[molecule]) for molecule in mols if me[molecule] >= 0})


def project(topology, source, attribute, indices="all"):
    """Deliver only stored hierarchy values and explicit memberships."""
    if source == "system":
        suffix = attribute.removeprefix("n_")
        if suffix in TABLES.values():
            return len(getattr(topology, suffix))
        if suffix == "atoms":
            return topology.n_atoms
        table, column, value = (
            ("groups", "group_type", GROUP_TYPES[suffix])
            if suffix in GROUP_TYPES
            else ("molecules", "molecule_type", MOLECULE_TYPES[suffix])
        )
        return int(getattr(topology, table)[column].eq(value).sum())
    if indices is None:
        return None
    axis = getattr(topology, TABLES[source])
    selected = (
        np.arange(len(axis), dtype=np.int64)
        if is_all(indices)
        else flat_axis(indices, "indices", "native hierarchy")
    )
    if isinstance(selected, str) or selected is None or np.any(selected >= len(axis)):
        raise ArgumentError(
            "indices", message="Hierarchy positions are outside the source axis."
        )
    context = {}
    output = []
    for index in selected:
        index = int(index)
        if attribute.startswith("n_"):
            kind = attribute[2:]
            if kind == "atoms":
                if source == "chain":
                    value = int(topology.atoms.chain_index.eq(index).sum())
                else:
                    groups = members(topology, source, index, "group", context=context)
                    value = int(topology.atoms.group_index.isin(groups).sum())
            elif kind in TABLES.values():
                target = next(name for name, plural in TABLES.items() if plural == kind)
                value = len(members(topology, source, index, target, context=context))
            else:
                target, column, expected = (
                    ("group", "group_type", GROUP_TYPES[kind])
                    if kind in GROUP_TYPES
                    else ("molecule", "molecule_type", MOLECULE_TYPES[kind])
                )
                wanted = members(topology, source, index, target, context=context)
                value = int(
                    getattr(topology, TABLES[target])
                    .iloc[wanted][column]
                    .eq(expected)
                    .sum()
                )
            output.append(value)
            continue
        target, field = attribute.split("_", 1)
        wanted = members(topology, source, index, target, context=context)
        values = (
            wanted
            if field == "index"
            else [
                _clean(getattr(topology, TABLES[target]).iloc[i][attribute])
                for i in wanted
            ]
        )
        scalar = (
            source == target
            or (source == "group" and target != "group")
            or (source == "molecule" and target in {"entity", "chain"})
        )
        output.append(
            values[0]
            if scalar and len(values) == 1
            else None
            if scalar and not values and source != "molecule"
            else values
        )
    return output


def query_rows(topology):
    """Build sparse hierarchy rows; unknown parent keys never join each other."""
    groups = topology.groups.copy()
    groups["group_index"] = pd.array(range(topology.n_groups), dtype="Int64")
    chain_members = by_chain(topology)
    relation = pd.DataFrame(
        {
            "group_index": pd.array(
                [int(group) for members in chain_members for group in members],
                dtype="Int64",
            ),
            "chain_index": pd.array(
                [chain for chain, members in enumerate(chain_members) for _ in members],
                dtype="Int64",
            ),
        }
    )
    rows = groups.merge(relation, on="group_index", how="left", sort=False)
    # Every parent table has a non-null positional key. Outer joins keep empty
    # declarations without equating unrelated missing child memberships.
    for name, key in [
        ("chains", "chain_index"),
        ("molecules", "molecule_index"),
        ("entities", "entity_index"),
    ]:
        table = getattr(topology, name).copy()
        table[key] = pd.array(range(len(table)), dtype="Int64")
        rows = rows.merge(table, on=key, how="outer", sort=False)
    return rows
