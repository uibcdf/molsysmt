"""Evaluate known native group hierarchy without manufacturing an atomic view."""

import inspect
import io
import tokenize

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError


def select_inventory(molecular_system, selection, element):
    from molsysmt.native import MolSys, Topology
    from molsysmt.native._chain_groups import uses_declared_hierarchy
    from molsysmt.native._group_hierarchy import query_rows

    candidates = (
        molecular_system
        if isinstance(molecular_system, (list, tuple))
        else [molecular_system]
    )
    topologies = [
        item.topology if isinstance(item, MolSys) else item
        for item in candidates
        if isinstance(item, (MolSys, Topology))
    ]
    if len(topologies) != 1:
        from molsysmt.basic import convert, get, has_attribute

        if has_attribute(molecular_system, "n_atoms", include_none=True):
            count = get(molecular_system, n_atoms=True)
            if count is not None and count > 0:
                return None
        topology = convert(molecular_system, to_form="molsysmt.Topology")
    else:
        topology = topologies[0]
    if not uses_declared_hierarchy(topology):
        return None
    tokens = list(tokenize.generate_tokens(io.StringIO(selection).readline))
    names = [
        token.string
        for index, token in enumerate(tokens)
        if token.type == tokenize.NAME
        and not (index and tokens[index - 1].string == "@")
    ]
    variable_names = [
        tokens[index + 1].string
        for index, token in enumerate(tokens[:-1])
        if token.string == "@" and tokens[index + 1].type == tokenize.NAME
    ]
    atomic_query = any(
        name.startswith(("atom_", "component_", "bond_"))
        or name in ("within", "bonded")
        for name in names
    )
    if atomic_query:
        if topology.n_atoms:
            return None
        raise StructuralInconsistencyError(
            reason="This selection needs an atomic inventory; only group hierarchy is represented."
        )
    from molsysmt.configure import selection_shortcuts

    from .molsysmt import (
        _column_has_integer_strings,
        _id_columns_with_numeric_comparisons,
    )

    expression = selection
    lines = selection.splitlines(keepends=True)
    offsets = np.concatenate(([0], np.cumsum([len(line) for line in lines])))
    shortcuts = selection_shortcuts["MolSysMT"]
    replacements = []
    for index, token in enumerate(tokens):
        if token.type != tokenize.NAME or token.string not in shortcuts:
            continue
        if index and tokens[index - 1].string == "@":
            continue
        start = int(offsets[token.start[0] - 1]) + token.start[1]
        end = int(offsets[token.end[0] - 1]) + token.end[1]
        replacements.append((start, end, "(" + shortcuts[token.string] + ")"))
    for start, end, expanded in reversed(replacements):
        expression = expression[:start] + expanded + expression[end:]
    local = {}
    if variable_names:
        frames = inspect.stack()
        try:
            for name in variable_names:
                for frame in frames:
                    if name in frame.frame.f_locals:
                        local[name] = frame.frame.f_locals[name]
                        break
                    if name in frame.frame.f_globals:
                        local[name] = frame.frame.f_globals[name]
                        break
                else:
                    raise ValueError(f"Selection variable @{name} is not defined.")
        finally:
            del frames
    rows = query_rows(topology)
    for column in _id_columns_with_numeric_comparisons(
        expression, [c for c in rows if c.endswith("_id")]
    ):
        if _column_has_integer_strings(rows[column]):
            rows[column] = pd.to_numeric(rows[column], errors="coerce")
    selected = rows.query(expression, engine="python", local_dict=local)
    return np.unique(selected[f"{element}_index"].dropna().astype(np.int64)).tolist()
