"""Receiving retained-axis native geometry setters and transformations.

Unit/selection validation belongs to MolSysMT. Shape checks here enforce the
receiver's retained-axis contract, not new scientific criteria or broadcasting.
"""


def _geometry_token(target):
    structures = target.structures
    return (
        id(structures),
        id(structures._coordinates),
        id(structures._box),
        id(target._interactions),
        tuple((name, id(result)) for name, result in target.interactions.items()),
    )


def _prepare_geometry_set(target, parameters, attributes):
    from molsysmt import basic
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.argdigest.argument.box import digest_box
    from molsysmt._private.argdigest.argument.coordinates import digest_coordinates
    from molsysmt._private.argdigest.argument.element import digest_element
    from molsysmt._private.variables import is_all
    from molsysmt.basic._index_validation import validate_structure_indices
    from molsysmt.native import MolSys

    if not isinstance(target, MolSys):
        raise TypeError("Managed geometry setting requires the bound native MolSys.")
    if hasattr(target, "_pending_interaction_edits"):
        raise ValueError("Managed setting cannot run inside an active molecular edit.")
    unsupported = attributes.keys() - {"coordinates", "box"}
    if unsupported:
        raise NotImplementedError(
            "Managed basic.set currently receives coordinates and box only; "
            f"unreceived attributes: {sorted(unsupported)}. Use native MolSysMT "
            "with explicit reconciliation for other effects."
        )
    caller = "molsysmt.basic.set.set"
    element = parameters["element"]
    if element is not None:
        element = digest_element(element, caller=caller)
    if attributes and element not in (None, "atom", "system"):
        raise ValueError(
            "Managed geometry setting requires element=None, atom or system."
        )
    if "box" in attributes and element == "atom":
        raise ValueError("Box assignment requires element=None or system.")
    frames = validate_structure_indices(target, parameters["structure_indices"], caller)
    n_structures = int(target.structures.n_structures)
    all_frames = is_all(frames)
    selected_frames = (
        list(range(n_structures))
        if all_frames
        else ([] if frames is None else list(frames))
    )
    atoms = None
    if "coordinates" in attributes:
        if element == "system":
            # A system-level native setter deliberately ignores atom selection.
            basic.get(
                target,
                structure_indices=parameters["structure_indices"],
                chemical_state=parameters["chemical_state"],
                n_atoms=True,
            )
            atoms = list(range(target.get_n_atoms()))
        else:
            atoms = basic.select(
                target,
                selection=parameters["selection"],
                structure_indices=parameters["structure_indices"],
                chemical_state=parameters["chemical_state"],
                syntax=parameters["syntax"],
            )
    elif attributes:
        # Validate the native chemical-state context before a system-level box
        # write, even though that context does not alter box values.
        basic.get(
            target,
            structure_indices=parameters["structure_indices"],
            chemical_state=parameters["chemical_state"],
            n_atoms=True,
        )

    values = dict(attributes)
    coordinate_write = bool(selected_frames) and atoms is not None and len(atoms) > 0
    box_write = bool(selected_frames) and "box" in values
    if values and n_structures == 0:
        raise ValueError(
            "Initialize structures through loading before managed geometry edits."
        )
    if "coordinates" in values:
        value = digest_coordinates(values["coordinates"], caller=caller)
        if coordinate_write:
            if value is None:
                raise ValueError(
                    "Managed coordinates must retain the current structure and atom axes."
                )
            shape = puw.get_value(value).shape
            if shape != (len(selected_frames), len(atoms), 3):
                raise ValueError(
                    "Coordinates must match the selected structure and atom axes; no broadcasting is added."
                )
        values["coordinates"] = value
    if "box" in values:
        value = digest_box(values["box"], caller=caller)
        if box_write:
            if value is None and not all_frames:
                raise ValueError(
                    "Clearing the box requires the native all-structures sentinel."
                )
            if value is not None and puw.get_value(value).shape != (
                len(selected_frames),
                3,
                3,
            ):
                raise ValueError(
                    "Box matrices must match the selected structure axis; no broadcasting is added."
                )
            if value is not None and not all_frames and target.structures._box is None:
                raise ValueError(
                    "Initialize the full box series before a partial replacement."
                )
        values["box"] = value
    return {
        "run": lambda: basic.set(target, **parameters, **values),
        "changed": coordinate_write or box_write,
        "interactions_policy": "preserve",
    }


def _prepare_geometry_transform(target, name, parameters):
    """Declare retained identities and let the public native tool own science."""
    from molsysmt import basic, structure
    from molsysmt._private.variables import is_all
    from molsysmt.basic._index_validation import validate_structure_indices
    from molsysmt.native import MolSys

    if name not in {
        "translate",
        "rotate",
        "flip",
        "least_rmsd_fit",
        "least_rmsd_align",
    }:
        raise NotImplementedError(
            f"Managed structure transform {name!r} is not received."
        )
    if not isinstance(target, MolSys):
        raise TypeError("Managed geometry transforms require the bound native MolSys.")
    if hasattr(target, "_pending_interaction_edits"):
        raise ValueError(
            "Managed transforms cannot run inside an active molecular edit."
        )
    frames = validate_structure_indices(
        target, parameters["structure_indices"], f"molsysmt.structure.{name}"
    )
    has_frames = (
        int(target.structures.n_structures) > 0
        if is_all(frames)
        else frames is not None and len(frames) > 0
    )
    # This checks participating-scope presence, not the exact moved population.
    # Native sequence alignment expands its anchors to complete components.
    atoms = basic.select(
        target,
        selection=parameters["selection"],
        structure_indices=parameters["structure_indices"],
        syntax=parameters["syntax"],
    )
    operation = getattr(structure, name)
    return {
        "run": lambda: operation(target, **parameters),
        "changed": bool(has_frames and atoms is not None and len(atoms) > 0),
        # Native setters invalidate the structures they actually publish.
        "interactions_policy": "preserve",
    }


def _run_geometry_transform(owner, name, parameters, update_view):
    """Preserve native independent outputs and serialize admitted bound edits."""
    from molsysmt import structure
    from molsysmt._private.argdigest.argument.in_place import digest_in_place

    if name not in {
        "translate",
        "rotate",
        "flip",
        "least_rmsd_fit",
        "least_rmsd_align",
    }:
        raise NotImplementedError(f"Structure transform {name!r} is not received.")
    in_place = digest_in_place(
        parameters["in_place"], caller=f"molsysviewer_molsysmt.structure.{name}"
    )
    if not isinstance(update_view, bool):
        raise TypeError("update_view must be a boolean.")
    owner._target()
    if not in_place:
        return owner._read(getattr(structure, name), parameters)
    view = owner._view_ref()
    coordinator = getattr(view.addons.manager, "system_edits", None)
    if coordinator is None:
        raise RuntimeError("This Viewer host lacks managed molecular-edit receiving.")
    return coordinator.execute(
        lambda target: _prepare_geometry_transform(target, name, parameters),
        name=f"molsysmt.structure.{name}",
        update_view=update_view,
        rejection_check=_geometry_token,
    )
