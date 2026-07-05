"""Runtime state for the MolSysMT MolSysViewer addon.

The runtime is the addon's public per-view state namespace, exposed as
``view.addons.molsysmt`` through ``AddonSpec.state_factory`` (see
:func:`create_molsysmt_state`). It holds session/UI state and result/tag
bookkeeping only. It does **not** own a molecular system: operations resolve the
system from the view-as-form at action time (see ``access.py``).

Older code may still reach the same object through the private
``view._molsysmt_addon_runtime`` attribute; it is the *same* instance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class _BasicNamespace:
    """Native MolSysViewer operations exposed under the MolSysMT addon facade."""

    def __init__(self, state: MolSysMTAddonRuntime) -> None:
        self._state = state

    def _view(self) -> Any:
        view = self._state._view
        if view is None:
            raise RuntimeError("MolSysMT addon state is not attached to a view.")
        return view

    @property
    def add(self) -> Any:
        """Alias to ``view.add``; MolSysViewer owns reconciliation."""
        return self._view().add

    @property
    def remove(self) -> Any:
        """Alias to ``view.remove``; MolSysViewer owns reconciliation."""
        return self._view().remove


class _EmptyNamespace:
    """Reserved facade namespace for upcoming MVP flows."""

    def __init__(self, state: MolSysMTAddonRuntime, name: str) -> None:
        self._state = state
        self.name = name


class _ShowNamespace:
    """Addon-native viewer overlays and render-side MolSysMT flows."""

    name = "show"

    def __init__(self, state: MolSysMTAddonRuntime) -> None:
        self._state = state

    def _view(self) -> Any:
        view = self._state._view
        if view is None:
            raise RuntimeError("MolSysMT addon state is not attached to a view.")
        return view

    def color_by(self, property: str = "charge", palette: Any = "viridis") -> Any:
        """Compute a MolSysMT scalar property and apply it as viewer colors."""
        from .adapters.color import property_values

        view = self._view()
        result = property_values(view, property)
        view.whole.set_color_by_values(
            result.values,
            element=result.element,
            palette=palette,
        )
        self._state.last_color_property = result.property
        self._state.last_color_element = result.element
        self._state.last_color_palette = palette
        record_event(view, "facade_color", property=result.property, element=result.element)
        return result

    def reset_colors(self) -> None:
        """Clear MolSysViewer per-atom color overrides for the whole view."""
        view = self._view()
        view.whole.reset_colors()
        self._state.last_color_property = None
        record_event(view, "facade_reset_colors")

    def contacts(
        self,
        *,
        selection: Any = "all",
        threshold: str = "4 angstroms",
        tag: str = "molsysmt-contacts",
        radius: Any = "0.08 nm",
        color: Any = 0x4499FF,
        alpha: float = 0.7,
    ) -> Any:
        """Compute MolSysMT contacts and render them as MolSysViewer links."""
        from .adapters.structure import contact_pairs

        view = self._view()
        result = contact_pairs(view, selection=selection, threshold=threshold)
        if result.atom_pairs:
            view.shapes.add_links(
                atom_pairs=result.atom_pairs,
                radius=radius,
                color=color,
                alpha=alpha,
                tag=tag,
                layer_tag="molsysmt-contacts",
            )
        else:
            view.shapes.clear(tag=tag)
        self._state.contacts_result = result
        self._state.contacts_tag = tag
        record_event(
            view,
            "facade_contacts",
            n_contacts=result.n_contacts,
            selection=selection,
            threshold=threshold,
            tag=tag,
        )
        return result

    def clear_contacts(self, tag: str | None = None) -> None:
        """Clear contact links created by the MolSysMT addon."""
        view = self._view()
        resolved_tag = tag or self._state.contacts_tag or "molsysmt-contacts"
        view.shapes.clear(tag=resolved_tag)
        if self._state.contacts_tag == resolved_tag:
            self._state.contacts_tag = None
        record_event(view, "facade_clear_contacts", tag=resolved_tag)

    def hbonds(
        self,
        *,
        tag: str = "msmt-hbonds",
        radius: Any = "0.1 nm",
        color: Any = 0x4499FF,
        alpha: float = 0.8,
    ) -> Any:
        """Compute Buch H-bonds and render them as structure-aware links."""
        from .adapters.hbonds import buch_hbond_links

        view = self._view()
        result = buch_hbond_links(view)
        if result.n_hbonds:
            view.shapes.links.add_hbonds(
                structures=result.structures,
                radius=radius,
                color=color,
                alpha=alpha,
                tag=tag,
            )
        else:
            view.shapes.clear(tag=tag)
        self._state.hbonds_result = result
        self._state.hbonds_tag = tag
        record_event(view, "facade_hbonds", n_hbonds=result.n_hbonds, tag=tag)
        return result

    def clear_hbonds(self, tag: str | None = None) -> None:
        """Clear H-bond links created by the MolSysMT addon."""
        view = self._view()
        resolved_tag = tag or self._state.hbonds_tag or "msmt-hbonds"
        view.shapes.clear(tag=resolved_tag)
        if self._state.hbonds_tag == resolved_tag:
            self._state.hbonds_tag = None
        record_event(view, "facade_clear_hbonds", tag=resolved_tag)

    def select(
        self,
        selection: Any = "all",
        *,
        element: str = "atom",
        tag: str = "molsysmt-selection",
        activate: bool = True,
        replace: bool = True,
    ) -> Any:
        """Run a MolSysMT selection and publish it as a viewer selection."""
        from .adapters.select import select_indices

        view = self._view()
        result = select_indices(view, selection=selection, element=element)
        if not result.atom_indices:
            raise ValueError("MolSysMT selection resolved to no atoms.")

        if replace and view.selections.contains(tag):
            view.selections.clear(tag=tag)
        selection_obj = view.selections.add(
            tag,
            atom_indices=result.atom_indices,
            skip_digestion=True,
        )
        if activate:
            selection_obj.activate()

        self._state.last_selection = selection
        self._state.last_selection_element = element
        self._state.last_selection_indices = result.indices
        self._state.last_selection_tag = tag
        record_event(
            view,
            "facade_select",
            selection=selection,
            element=element,
            n_selected=result.n_selected,
            n_atoms=len(result.atom_indices),
            tag=tag,
        )
        return result

    def clear_selection(self, tag: str | None = None) -> None:
        """Clear the MolSysMT active/persistent viewer selection."""
        view = self._view()
        resolved_tag = tag or self._state.last_selection_tag or "molsysmt-selection"
        if view.selections.contains(resolved_tag):
            view.selections.clear(tag=resolved_tag)
        view.active_selection.clear()
        if self._state.last_selection_tag == resolved_tag:
            self._state.last_selection_tag = None
        record_event(view, "facade_clear_selection", tag=resolved_tag)


@dataclass
class MolSysMTAddonRuntime:
    # Core
    enabled: bool = False
    workspace: str = "molsysmt"
    last_context_action: dict[str, Any] | None = None
    event_log: list[dict[str, Any]] = field(default_factory=list)

    # Basic panel: system inspection
    n_atoms: int | None = None
    n_residues: int | None = None
    n_chains: int | None = None
    n_frames: int | None = None

    # Basic panel: MolSysMT selection flow
    last_selection: str | None = None
    last_selection_element: str = "atom"
    last_selection_indices: list[int] | None = None
    last_selection_tag: str | None = None

    # Color panel
    last_color_property: str | None = None
    last_color_element: str = "group"
    last_color_palette: str = "viridis"

    # Structure panel
    contacts_result: Any = None
    contacts_tag: str | None = None
    rmsd_result: Any = None
    rmsf_result: Any = None
    pca_result: Any = None

    # H-Bonds panel
    hbonds_result: Any = None
    hbonds_tag: str | None = None

    # Topology panel
    bondgraph_result: Any = None
    dihedral_quartets_result: Any = None

    # PBC panel
    pbc_status: bool | None = None

    # Mechanics panel
    forces_result: Any = None
    energy_result: Any = None
    forces_tag: str | None = None

    # Build panel
    last_build_op: str | None = None
    build_log: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._view = None
        self.basic = _BasicNamespace(self)
        self.structure = _EmptyNamespace(self, "structure")
        self.show = _ShowNamespace(self)
        self.overlays = self.show

    def __getitem__(self, key: str) -> Any:
        # Backward compatibility with dict-based lookups (per the addon docs).
        return getattr(self, key)

    def attach_view(self, view: Any) -> MolSysMTAddonRuntime:
        """Attach or refresh the owning view back-reference."""
        self._view = view
        return self


def create_molsysmt_state(view: Any) -> MolSysMTAddonRuntime:
    """``AddonSpec.state_factory`` for ``view.addons.molsysmt``.

    Returns the per-view runtime, reusing one already stored on the legacy
    private attribute so state seeded during early lifecycle hooks is not
    overwritten. Also keeps ``view._molsysmt_addon_runtime`` pointing at the same
    instance for backward compatibility.
    """
    runtime = getattr(view, "_molsysmt_addon_runtime", None)
    if isinstance(runtime, MolSysMTAddonRuntime):
        runtime.attach_view(view)
        return runtime
    state = MolSysMTAddonRuntime().attach_view(view)
    try:
        view._molsysmt_addon_runtime = state
    except Exception:
        pass
    return state


def ensure_runtime(view: Any) -> MolSysMTAddonRuntime:
    """Return the MolSysMT runtime for ``view``.

    Prefers the public ``view.addons.molsysmt`` namespace (lazily created by the
    ``state_factory`` when the addon is registered), and falls back to the legacy
    private ``view._molsysmt_addon_runtime`` attribute so test doubles without an
    addons manager still work. Both point at the same object.
    """
    addons = getattr(view, "addons", None)
    if addons is not None:
        try:
            namespace = getattr(addons, "molsysmt", None)
        except Exception:
            namespace = None
        if isinstance(namespace, MolSysMTAddonRuntime):
            namespace.attach_view(view)
            try:
                view._molsysmt_addon_runtime = namespace
            except Exception:
                pass
            return namespace

    runtime = getattr(view, "_molsysmt_addon_runtime", None)
    if not isinstance(runtime, MolSysMTAddonRuntime):
        runtime = MolSysMTAddonRuntime()
        try:
            view._molsysmt_addon_runtime = runtime
        except Exception:
            pass
    runtime.attach_view(view)
    return runtime


def record_event(view: Any, event: str, **payload: Any) -> MolSysMTAddonRuntime:
    runtime = ensure_runtime(view)
    runtime.event_log.append({"event": event, **payload})
    return runtime
