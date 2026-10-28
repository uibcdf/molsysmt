"""Receive reviewed native prefix additions; molecular science stays native."""


def _composition_token(target):
    """Observe native candidate publication, including replaced structural fields.

    Native add prepares independent domains; Structures.append prepares every
    series before replacing its owned payload. Do not infer rejection safety
    from unchanged counts or MolSys dictionary identity alone.
    """
    return (
        id(target.topology),
        id(target.structures),
        id(target.molecular_mechanics),
        id(target._interactions),
        id(target._structure_chemical_state_indices),
        tuple(
            (key, id(value)) for key, value in sorted(vars(target.structures).items())
        ),
    )


def _prepare_composition(target, name, parameters):
    from molsysmt import basic
    from molsysmt._private.argdigest.argument.structure_indices import (
        digest_structure_indices,
    )
    from molsysmt._private.variables import is_all
    from molsysmt.basic._index_validation import validate_structure_indices
    from molsysmt.native import MolSys

    if not isinstance(target, MolSys):
        raise TypeError("Managed composition requires the bound native MolSys.")
    if hasattr(target, "_pending_interaction_edits"):
        raise ValueError(
            "Managed composition cannot run inside an active molecular edit."
        )
    source = parameters["from_molecular_system"]
    if name == "add":
        selection = parameters["selection"]
        if is_all(selection):
            added = basic.get(source, n_atoms=True)
        else:
            selected = basic.select(
                source, selection=selection, syntax=parameters["syntax"]
            )
            added = 0 if selected is None else len(selected)
    elif name == "append_structures":
        caller = "molsysmt.basic.append_structures.append_structures"
        frames = digest_structure_indices(
            parameters["structure_indices"], caller=caller
        )
        frames = validate_structure_indices(source, frames, caller)
        added = (
            basic.get(source, n_structures=True)
            if is_all(frames)
            else (0 if frames is None else len(frames))
        )
    else:
        raise ValueError("Unreceived molecular composition operation.")
    return {
        "run": lambda: getattr(basic, name)(target, **parameters),
        # Even empty additions may change native attributes/assignment reports.
        "changed": True,
        "added_count": int(added),
        "interactions_policy": "preserve",
    }


def _compose_bound(owner, name, parameters, update_view):
    from molsysmt import basic
    from molsysmt._private.argdigest.argument.in_place import digest_in_place

    in_place = digest_in_place(
        parameters["in_place"], caller=f"molsysviewer_molsysmt.basic.{name}"
    )
    if not isinstance(update_view, bool):
        raise TypeError("update_view must be a boolean.")
    if not in_place:
        return owner._read(getattr(basic, name), parameters)
    owner._target()
    view = owner._view()
    coordinator = getattr(view.addons.manager, "system_edits", None)
    if coordinator is None:
        raise RuntimeError("This Viewer host lacks managed composition receiving.")
    # This explicit keyword rejects older retained-axis hosts before science.
    return coordinator.execute(
        lambda target: _prepare_composition(target, name, parameters),
        name=f"molsysmt.basic.{name}",
        update_view=update_view,
        axis_growth="atoms" if name == "add" else "structures",
        rejection_check=_composition_token,
    )
