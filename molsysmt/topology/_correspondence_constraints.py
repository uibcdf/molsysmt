"""Validate index constraints and apply them inside compiled graph matching."""

import json

import numpy as np

from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


def normalize_pairs(value, name, caller):
    """Keep nonnegative, injective integer pairs without silently coercing labels."""
    try:
        pairs = np.asarray(value)
        if pairs.size == 0 and pairs.ndim == 1:
            pairs = np.empty((0, 2), dtype=np.int64)
        if (
            pairs.ndim != 2
            or pairs.shape[1] != 2
            or pairs.dtype.kind not in "iu"
            or np.any(pairs < 0)
            or np.any(pairs > np.iinfo(np.int64).max)
            or any(len(np.unique(pairs[:, axis])) != len(pairs) for axis in (0, 1))
            or (
                not isinstance(value, np.ndarray)
                and any(
                    isinstance(item, (bool, np.bool_)) for row in value for item in row
                )
            )
        ):
            raise ValueError("Invalid index pairs")
        return np.array(pairs[np.argsort(pairs[:, 0])], dtype=np.int64, copy=True)
    except (TypeError, ValueError, OverflowError) as error:
        raise ArgumentError(name, caller=caller) from error


def normalize_candidates(value, caller):
    """Accept one complete map or an explicit nonempty collection of maps."""
    name = "candidate_atom_correspondences"
    try:
        table = np.asarray(value)
        if table.ndim == 2:
            table = table[None]
            values = [value]
        else:
            values = value
        if (
            table.ndim != 3
            or table.shape[2] != 2
            or not table.shape[0]
            or not table.shape[1]
        ):
            raise ValueError("Supply at least one nonempty map")
        return np.stack([normalize_pairs(row, name, caller) for row in values])
    except (TypeError, ValueError, OverflowError) as error:
        raise ArgumentError(name, caller=caller) from error


def prepare_constraints(first, second, fixed, candidates, caller):
    """Check component scope, selected populations and compatibility of declarations."""
    fixed = (
        np.empty((0, 2), dtype=np.int64)
        if fixed is None
        else normalize_pairs(fixed, "fixed_atom_correspondence", caller)
    )
    if (
        not np.isin(fixed[:, 0], first.atoms).all()
        or not np.isin(fixed[:, 1], second.atoms).all()
    ):
        raise ArgumentError("fixed_atom_correspondence", caller=caller)
    if candidates is None:
        return fixed, None
    candidates = normalize_candidates(candidates, caller)
    for mapping in candidates:
        if not np.array_equal(mapping[:, 0], first.selected) or not np.array_equal(
            np.sort(mapping[:, 1]), second.selected
        ):
            raise ArgumentError("candidate_atom_correspondences", caller=caller)
        declared = dict(mapping.tolist())
        if any(
            (int(left) in declared and declared[int(left)] != right)
            or (right in declared.values() and declared.get(int(left)) != right)
            for left, right in fixed
        ):
            raise ArgumentError("candidate_atom_correspondences", caller=caller)
    # Canonical query order is shared. np.unique also sorts the projected maps.
    order = np.unique(candidates[:, :, 1], axis=0)
    result = np.empty((len(order), len(first.selected), 2), dtype=np.int64)
    result[:, :, 0], result[:, :, 1] = first.selected, order
    return fixed, result


def constrained_matches(first, second, pins, limit, *, exact=False):
    """Use RDKit atom properties to prune the search before completed matches exist."""
    from rdkit import Chem

    if len(first.atoms) != len(second.atoms) or len(first.selected) != len(
        second.selected
    ):
        return ()
    parameters = Chem.SubstructMatchParameters()
    parameters.uniquify = False
    parameters.useChirality = True
    parameters.maxMatches = int(limit)
    query, reference = first.molecule, second.molecule
    if len(pins) or exact:
        query, reference = Chem.Mol(query), Chem.Mol(reference)
        property_name = "_MolSysMTCorrespondenceConstraint"
        for graph, molecule, column in ((first, query, 0), (second, reference, 1)):
            anchors = dict(zip(pins[:, column].tolist(), range(len(pins))))
            selected = set(graph.selected.tolist())
            for position, source_index in enumerate(graph.atoms):
                label = [anchors.get(int(source_index), -1)]
                if exact:
                    label.extend(
                        [graph.labels[position], int(source_index) in selected]
                    )
                molecule.GetAtomWithIdx(position).SetProp(
                    property_name, json.dumps(label)
                )
            if exact:
                for (left, right), label in graph.edges.items():
                    molecule.GetBondBetweenAtoms(left, right).SetProp(
                        property_name, json.dumps(label)
                    )
        parameters.atomProperties = [property_name]
        if exact:
            parameters.bondProperties = [property_name]
    return reference.GetSubstructMatches(query, parameters)


def candidate_witness(first, second, fixed, candidate, caller):
    """Find a canonical complete-context extension without enumerating its H permutations."""
    pins = dict(fixed.tolist())
    pins.update(dict(candidate.tolist()))

    def match():
        pairs = np.array(sorted(pins.items()), dtype=np.int64).reshape(-1, 2)
        return constrained_matches(first, second, pairs, 1, exact=True)

    matches = match()
    if not matches or not first.admits(second, matches[0]):
        raise StructuralInconsistencyError(
            reason="A supplied map has no chemically admitted complete-context extension respecting the anchors.",
            caller=caller,
        )
    witness = matches[0]
    # Greedily fix the smallest feasible target for each unpinned context atom.
    # Each probe returns at most one witness; no factorial H-permutation table.
    for position, source_index in enumerate(first.atoms):
        source_index = int(source_index)
        if source_index in pins:
            continue
        chosen = int(second.atoms[witness[position]])
        occupied = set(pins.values())
        for target in second.atoms[second.atoms < chosen]:
            target = int(target)
            if target in occupied:
                continue
            pins[source_index] = target
            matches = match()
            if matches:
                witness, chosen = matches[0], target
                break
        pins[source_index] = chosen
    return witness
