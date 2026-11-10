"""Receive native graph and atom-axis edits without duplicating science."""


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


def _prepare_reconcile_protonation(target, parameters):
    """Receive one public native decision and its explicit correspondence."""
    from molsysmt import build

    assessment = build.assess_protonation(
        target,
        pH=parameters["pH"],
        engine=parameters["engine"],
        skip_digestion=parameters["skip_digestion"],
    )
    return _prepare_assessed_protonation(
        target, assessment, skip_digestion=parameters["skip_digestion"]
    )


def _prepare_assessed_protonation(target, assessment, *, skip_digestion=False):
    """Receive one already reviewed native decision without reassessing it."""
    import numpy as np

    from molsysmt.native import MolSys

    if not isinstance(target, MolSys):
        raise TypeError(
            "Managed protonation reconciliation requires the bound native MolSys."
        )
    report = assessment.to_dict()
    if report.get("schema") != "molsysmt.protonation_assessment@1":
        raise ValueError("Unsupported native protonation-assessment report.")
    atom_map = report["atom_map"]
    keep = atom_map["output_to_source_atom_indices"]
    reverse = atom_map["source_to_output_atom_indices"]
    structures = report["structure_indices"]
    count = int(target.get_n_atoms())
    frame_count = int(target.structures.n_structures)
    if (
        not all(
            isinstance(axis, np.ndarray)
            and axis.ndim == 1
            and axis.dtype == np.dtype("int64")
            for axis in (keep, reverse, structures)
        )
        or reverse.shape != (count,)
        or np.any(keep < 0)
        or np.any(keep >= count)
        or len(np.unique(keep)) != len(keep)
        or np.any(reverse < -1)
        or np.any(reverse >= len(keep))
        or np.count_nonzero(reverse >= 0) != len(keep)
        or not np.array_equal(reverse[keep], np.arange(len(keep)))
        or not np.array_equal(structures, np.arange(frame_count))
    ):
        raise ValueError(
            "The native protonation assessment has incompatible atom or structure maps."
        )
    changed = len(keep) != count or not np.array_equal(keep, np.arange(count))
    return {
        "run": lambda: assessment.apply(
            target, in_place=True, skip_digestion=skip_digestion
        ),
        "changed": bool(changed),
        "atom_index_map": {int(old): new for new, old in enumerate(keep)}
        if changed
        else None,
        "interactions_policy": "preserve",
        # Native apply stages the full subset before its single dictionary
        # publication. The host also checks that dictionary on rejection.
        "failure_atomic": True,
    }


def _run_reconcile_protonation(owner, parameters, update_view):
    from molsysmt import build
    from molsysmt._private.argdigest.argument.in_place import digest_in_place

    in_place = digest_in_place(
        parameters["in_place"],
        caller="molsysviewer_molsysmt.build.reconcile_protonation",
    )
    if not isinstance(update_view, bool):
        raise TypeError("update_view must be a boolean.")
    owner._target()
    if not in_place:
        return owner._read(build.reconcile_protonation, parameters)
    coordinator = getattr(owner._view_ref().addons.manager, "system_edits", None)
    if coordinator is None:
        raise RuntimeError("This Viewer host lacks managed molecular-edit receiving.")
    return coordinator.execute(
        lambda target: _prepare_reconcile_protonation(target, parameters),
        name="molsysmt.build.reconcile_protonation",
        update_view=update_view,
    )
