"""Sharing selection and projection boundaries between PDBQT file/string forms."""

from molsysmt._private.pdbqt import PREFIX, fail, read
from molsysmt._private.variables import is_all


def selected_native(
    item, atom_indices, structure_indices, discard_torsion_tree, *, text
):
    from molsysmt.native import PDBQTFileHandler

    with PDBQTFileHandler(
        item, storage_mode="resident" if text else "indexed"
    ) as handler:
        return handler._to_native(atom_indices, structure_indices, discard_torsion_tree)


def selected_payload(item, atom_indices, structure_indices, *, text):
    from molsysmt.native import PDBQTFileHandler

    with PDBQTFileHandler(
        item, storage_mode="resident" if text else "indexed"
    ) as handler:
        return handler._payload(atom_indices, structure_indices)


def write_payload(payload, output_filename):
    from pathlib import Path

    if output_filename is None:
        fail("PDBQT file output requires an output_filename.")
    Path(output_filename).write_text(payload, encoding="utf-8", newline="")
    return output_filename


def as_text(payload):
    return PREFIX + payload


def restore_export_axis(mapping, source, atoms, structures):
    """Restore a completed writer map onto the full caller atom/structure axes."""
    import numpy as np

    from molsysmt.chemical_states._chemical_graph import chemical_graph_digest

    n_atoms = source.topology.n_atoms
    retained = (
        np.arange(n_atoms, dtype=np.int64)
        if atoms is None or is_all(atoms)
        else np.unique(atoms)
    )
    mapping["output_to_source_atom_indices"] = retained[
        mapping["output_to_source_atom_indices"]
    ]
    forward = np.full(n_atoms, -1, dtype=np.int64)
    forward[mapping["output_to_source_atom_indices"]] = np.arange(
        mapping["n_output_atoms"], dtype=np.int64
    )
    mapping["source_to_output_atom_indices"] = forward
    mapping["n_source_atoms"] = n_atoms
    for field, column in (
        ("source_atom_ids", "atom_id"),
        ("source_atom_names", "atom_name"),
        ("source_atom_types", "atom_type"),
    ):
        values = source.topology.atoms[column]
        mapping[field] = (
            values.astype(object).where(values.notna(), None).to_numpy(copy=True)
        )
    mapping["source_chemical_digest"] = (
        None
        if mapping["chemical_state_index"] is None
        else chemical_graph_digest(source, mapping["chemical_state_index"])
    )
    mapping["source_atom_status"] = np.where(forward >= 0, "retained", "omitted")
    mapping["ordered_root_source_atom_indices"] = retained[
        mapping["ordered_root_source_atom_indices"]
    ]
    first = mapping["first_root_source_atom_index"]
    if first is not None:
        mapping["first_root_source_atom_index"] = int(retained[first])
    mapping["branch_source_atom_pairs"] = retained[mapping["branch_source_atom_pairs"]]
    mapping["source_structure_indices"] = (
        np.arange(source.structures.n_structures, dtype=np.int64)
        if structures is None or is_all(structures)
        else np.asarray(structures, dtype=np.int64).copy()
    )
    return mapping


def structure_count(item, structure_indices, *, text):
    from molsysmt.native import PDBQTFileHandler

    with PDBQTFileHandler(
        item, storage_mode="resident" if text else "indexed"
    ) as handler:
        return len(
            handler._axis(structure_indices, handler.n_structures, "structure_indices")
        )


def full_projection(n_atoms, atom_indices, structure_indices, *, n_structures=1):
    import numpy as np

    atoms_full = is_all(atom_indices) or np.array_equal(
        np.unique(atom_indices), np.arange(n_atoms)
    )
    frames_full = is_all(structure_indices) or np.array_equal(
        structure_indices, np.arange(n_structures)
    )
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
    from molsysmt.native import PDBQTFileHandler

    with (
        item.copy()
        if source_form == "molsysmt.PDBQTFileHandler"
        else PDBQTFileHandler(
            item, storage_mode="indexed" if source_form == "file:pdbqt" else "resident"
        )
    ) as handler:
        atoms = select(handler._native(), selection=selection, syntax=syntax)
        structures = handler._axis(
            structure_indices, handler.n_structures, "structure_indices"
        )
        return full_projection(
            handler.n_atoms, atoms, structures, n_structures=handler.n_structures
        )
