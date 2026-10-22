"""Publishing prepared native subsets without exposing misaligned domains."""

import weakref


def validate_removal_target(target, to_form):
    """Reject unsupported in-place targets before preparing an extraction."""
    from molsysmt._private.smonitor import ArgumentError

    from .molsys import MolSys
    from .structures import Structures
    from .topology import Topology

    caller = "molsysmt.basic.remove"
    if to_form is not None:
        raise ArgumentError(
            "to_form",
            value=to_form,
            caller=caller,
            message="In-place removal cannot convert forms; leave to_form=None.",
        )
    if not isinstance(target, (MolSys, Topology, Structures)):
        raise ArgumentError(
            "in_place",
            value=True,
            caller=caller,
            message=(
                "In-place removal requires a native MolSys or standalone "
                "Topology/Structures. Use in_place=False for other forms "
                "or complementary inputs."
            ),
        )
    owner_ref = getattr(target, "_molsys_owner_ref", None)
    if owner_ref is not None and owner_ref() is not None:
        raise ArgumentError(
            "molecular_system",
            value=target,
            caller=caller,
            message=(
                "An attached domain cannot be resized independently; "
                "remove from its owning MolSys or use in_place=False."
            ),
        )
    if hasattr(target, "_pending_interaction_edits"):
        raise ArgumentError(
            "molecular_system",
            value=target,
            caller=caller,
            message="In-place removal cannot run inside an active molecular edit.",
        )


def publish_subset(target, candidate):
    """Adopt prepared molecular data, retaining the target and its extension state.

    Extraction owns projection and validation. All allocating preparation here
    precedes publication. Old domains become detached snapshots; no coordinate
    setter or intermediate chemical replacement sees inconsistent axes.
    """
    from .molsys import MolSys

    state = vars(target).copy()
    state.update(vars(candidate))
    if isinstance(target, MolSys):
        old_domains = target.topology, target.structures, target.chemical_states
        new_domains = (
            candidate.topology,
            candidate.structures,
            candidate.chemical_states,
        )
        owner_ref = weakref.ref(target)
        for domain in new_domains:
            if domain is not None:
                object.__setattr__(domain, "_molsys_owner_ref", owner_ref)
    else:
        old_domains = ()

    object.__setattr__(target, "__dict__", state)
    for domain in old_domains:
        if domain is not None:
            object.__setattr__(domain, "_molsys_owner_ref", None)
