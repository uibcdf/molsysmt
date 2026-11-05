"""Receive atomic native graph publication without calculating chemistry twice."""


def _bond_publication_token(target):
    """Observe fields published by the reviewed native bond writer, not caches.

    The native writer prepares replacement tables and analysis invalidation
    before publication. Empty candidates publish nothing. This bounded token
    copies neither molecular tables nor trajectory/analysis arrays; it is not
    an observer for arbitrary external or raw-array edits.
    """
    states = target.chemical_states
    return (
        id(states),
        states._reference_index,
        tuple(
            (
                id(state),
                id(state.bonds),
                id(state.components),
                id(state.component_indices),
                state.connectivity_completeness,
                state.component_completeness,
            )
            for state in states._states
        ),
        id(target._interactions),
        tuple((name, id(result)) for name, result in target.interactions.items()),
    )


def _prepare_add_missing_bonds(target, parameters):
    from molsysmt import build
    from molsysmt.native import MolSys

    if not isinstance(target, MolSys):
        raise TypeError("Managed bond addition requires the bound native MolSys.")
    if hasattr(target, "_pending_interaction_edits"):
        raise ValueError(
            "Managed bond addition cannot run inside an active molecular edit."
        )
    before = _bond_publication_token(target)

    def run():
        result = build.add_missing_bonds(target, **parameters)
        # Finalize the trusted plan only after the single native call. Counts
        # cannot establish no-op or correspondence; atomic publication can.
        plan["changed"] = _bond_publication_token(target) != before
        return result

    plan = {
        "run": run,
        "changed": False,
        # Native graph publication already invalidates all named analyses.
        "interactions_policy": "preserve",
    }
    return plan


def _run_add_missing_bonds(owner, parameters, update_view):
    from molsysmt import build
    from molsysmt._private.argdigest.argument.in_place import digest_in_place

    in_place = digest_in_place(
        parameters["in_place"], caller="molsysviewer_molsysmt.build.add_missing_bonds"
    )
    if not isinstance(update_view, bool):
        raise TypeError("update_view must be a boolean.")
    owner._target()
    if not in_place:
        return owner._read(build.add_missing_bonds, parameters)
    coordinator = getattr(owner._view_ref().addons.manager, "system_edits", None)
    if coordinator is None:
        raise RuntimeError("This Viewer host lacks managed molecular-edit receiving.")
    return coordinator.execute(
        lambda target: _prepare_add_missing_bonds(target, parameters),
        name="molsysmt.build.add_missing_bonds",
        update_view=update_view,
        rejection_check=_bond_publication_token,
    )
