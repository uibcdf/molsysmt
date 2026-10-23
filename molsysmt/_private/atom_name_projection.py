"""Projecting selected labels into a bounded, group-local name namespace."""

import string

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

CALLER = "molsysmt.form.project_atom_names"
ALPHABET = string.digits + string.ascii_uppercase


def fits(value, width):
    return (
        isinstance(value, str)
        and 0 < len(value) <= width
        and value.isascii()
        and all(33 <= ord(char) <= 126 for char in value)
    )


def base36(number):
    if number == 0:
        return "0"
    text = ""
    while number:
        number, remainder = divmod(number, 36)
        text = ALPHABET[remainder] + text
    return text


def project_labels(names, groups, selected, width):
    """Reserve valid names first; allocate monotonically within each group/stem."""
    reserved = {}
    for name, group in zip(names, groups):
        if fits(name, width):
            reserved.setdefault(group, set()).add(name)
    counters = {}
    output = names.copy()
    changed = []
    for index in selected:
        name, group = names[index], groups[index]
        if fits(name, width):
            continue
        stem = next(
            (char.upper() for char in name or "" if char in string.ascii_letters),
            "X",
        )
        used = reserved.setdefault(group, set())
        key = (group, stem)
        counter = counters.get(key, 0)
        while counter < 36 ** (width - 1):
            candidate = stem + base36(counter)
            counter += 1
            if candidate not in used:
                break
        else:
            raise StructuralInconsistencyError(
                reason=f"The {width}-column name namespace for prefix {stem!r} in group {group} is exhausted; no names were applied.",
                caller=CALLER,
            )
        used.add(candidate)
        counters[key] = counter
        output[index] = candidate
        changed.append(index)
    return output, np.asarray(changed, dtype=np.int64)


def project(molecular_system, to_form, selection, return_report, syntax):
    from molsysmt import __version__
    from molsysmt.basic import convert, select
    from molsysmt.basic import set as set_attributes
    from molsysmt.native import MolSys

    if to_form not in ("file:pdbqt", "string:pdbqt_text"):
        raise ArgumentError(
            "to_form",
            value=to_form,
            caller=CALLER,
            message="Name projection currently supports file:pdbqt and string:pdbqt_text.",
        )
    source = (
        molecular_system
        if isinstance(molecular_system, MolSys)
        else convert(molecular_system, to_form="molsysmt.MolSys")
    )
    if source.topology is None:
        raise StructuralInconsistencyError(
            reason="Atom-name projection requires topology with an indexed atom/group axis.",
            caller=CALLER,
        )
    atoms = source.topology.atoms
    groups = atoms["group_index"].to_numpy()
    if any(
        not pd.isna(group)
        and (
            isinstance(group, (bool, np.bool_))
            or not isinstance(group, (int, np.integer))
            or not 0 <= group < source.topology.n_groups
        )
        for group in groups
    ):
        raise StructuralInconsistencyError(
            reason="Known group indices must lie within the native group axis.",
            caller=CALLER,
        )
    scope = "group"
    if any(pd.isna(group) for group in groups):
        # Unknown grouping cannot justify separate namespaces. Reserve names
        # across the entire system rather than inventing group memberships.
        groups = np.zeros(len(atoms), dtype=np.int64)
        scope = "system"
    if selection is None:
        raise ArgumentError("selection", value=selection, caller=CALLER)
    selected = np.asarray(select(source, selection=selection, syntax=syntax))
    if selected.ndim != 1 or (selected.size and selected.dtype.kind not in "iu"):
        raise ArgumentError(
            "selection",
            value=selection,
            caller=CALLER,
            message="Name projection requires one flat atom selection, not structure-dependent populations.",
        )
    selected = np.unique(selected).astype(np.int64)
    names = np.asarray(
        [None if pd.isna(value) else str(value) for value in atoms["atom_name"]],
        dtype=object,
    )
    ids = np.asarray(
        [None if pd.isna(value) else str(value) for value in atoms["atom_id"]],
        dtype=object,
    )
    output_names, changed = project_labels(names, groups, selected, width=4)
    # Native copying owns mutable domains; protected geometry blocks stay shared
    # until a later managed edit. No trajectory-sized geometry copy is needed.
    output = source.copy(deep=False)
    if len(changed):
        set_attributes(output, selection=changed, atom_name=output_names[changed])
    if not return_report:
        return output
    axis = np.arange(len(atoms), dtype=np.int64)
    report = dict(
        schema="molsysmt.atom_map@1",
        operation="atom_name_projection",
        method="preserve_or_base36",
        parameters=dict(
            to_form=to_form,
            name_width=4,
            collision_scope=scope,
            existing_valid_duplicates="preserve",
        ),
        software={"molsysmt": __version__},
        n_source_atoms=len(atoms),
        n_output_atoms=len(atoms),
        source_to_output_atom_indices=axis.copy(),
        output_to_source_atom_indices=axis.copy(),
        source_atom_ids=ids.copy(),
        output_atom_ids=ids.copy(),
        source_atom_names=names.copy(),
        output_atom_names=output_names.copy(),
        selected_atom_indices=selected.copy(),
        renamed_atom_indices=changed.copy(),
    )
    return {"molecular_system": output, "report": report}
