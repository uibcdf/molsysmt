"""Sharing selection and projection boundaries between PDBQT file/string forms."""

from molsysmt._private.pdbqt import PREFIX, fail, read, to_native
from molsysmt._private.variables import is_all


def selected_native(
    item, atom_indices, structure_indices, discard_torsion_tree, *, text
):
    from molsysmt.basic._index_validation import (
        validate_element_indices,
        validate_structure_indices,
    )
    from molsysmt.form.molsysmt_MolSys.extract import extract

    output = to_native(read(item, text=text), discard_torsion_tree=discard_torsion_tree)
    atoms = validate_element_indices(
        output, atom_indices, "atom", "atom_indices", "PDBQT"
    )
    frames = validate_structure_indices(output, structure_indices, "PDBQT")
    if not is_all(atoms) or not is_all(frames):
        output = extract(output, atom_indices=atoms, structure_indices=frames)
    return output


def selected_payload(item, atom_indices, structure_indices, *, text):
    from molsysmt._private.pdbqt_writer import serialize
    from molsysmt.basic._index_validation import (
        validate_element_indices,
        validate_structure_indices,
    )
    from molsysmt.form.molsysmt_MolSys.extract import extract

    record = read(item, text=text)
    if is_all(atom_indices) and is_all(structure_indices):
        return record["payload"]
    native = to_native(record, discard_torsion_tree=True)
    atoms = validate_element_indices(
        native, atom_indices, "atom", "atom_indices", "PDBQT"
    )
    frames = validate_structure_indices(native, structure_indices, "PDBQT")
    if full_projection(native.topology.n_atoms, atoms, frames):
        return record["payload"]
    if record["torsion_tree"] is not None:
        fail(
            "PDBQT tree projection requires an explicitly remapped torsion_tree and native writer. Identity copies preserve the original tree."
        )
    selected = extract(native, atom_indices=atoms, structure_indices=frames)
    return serialize(selected, typing_scheme="autodock4")


def write_payload(payload, output_filename):
    from pathlib import Path

    if output_filename is None:
        fail("PDBQT file output requires an output_filename.")
    Path(output_filename).write_text(payload, encoding="utf-8", newline="")
    return output_filename


def as_text(payload):
    return PREFIX + payload


def structure_count(item, structure_indices, *, text):
    import numpy as np

    from molsysmt._private.smonitor import ArgumentError

    read(item, text=text)
    if is_all(structure_indices):
        return 1
    indices = np.asarray(structure_indices)
    if (
        indices.ndim != 1
        or (indices.size and indices.dtype.kind not in "iu")
        or np.any(indices != 0)
    ):
        raise ArgumentError(
            "structure_indices", value=structure_indices, caller="PDBQT"
        )
    return len(indices)


def full_projection(n_atoms, atom_indices, structure_indices):
    import numpy as np

    atoms_full = is_all(atom_indices) or np.array_equal(
        np.unique(atom_indices), np.arange(n_atoms)
    )
    frames_full = is_all(structure_indices) or np.array_equal(structure_indices, [0])
    return atoms_full and frames_full


def atom_attribute(item, attribute, indices, *, text):
    import numpy as np

    from molsysmt._private.smonitor import ArgumentError

    record = read(item, text=text)
    values = np.asarray([atom[attribute] for atom in record["atoms"]])
    if is_all(indices):
        return values
    indices = np.asarray(indices)
    if (
        indices.ndim != 1
        or (indices.size and indices.dtype.kind not in "iu")
        or np.any(indices < 0)
        or np.any(indices >= len(values))
    ):
        raise ArgumentError("indices", value=indices, caller="PDBQT")
    return values[indices.astype(np.int64)]


def identity_selection(item, source_form, selection, structure_indices, syntax):
    """Check semantic identity, including explicit complete index selections."""
    from molsysmt.basic import select
    from molsysmt.basic._index_validation import validate_structure_indices

    if is_all(selection) and is_all(structure_indices):
        return True
    native = to_native(
        read(item, text=source_form == "string:pdbqt_text"), discard_torsion_tree=True
    )
    atoms = select(native, selection=selection, syntax=syntax)
    frames = validate_structure_indices(native, structure_indices, "PDBQT")
    return full_projection(native.topology.n_atoms, atoms, frames)
