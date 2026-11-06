"""Selection review and managed removal over the existing expert edit adapter."""

from dataclasses import dataclass
from secrets import token_urlsafe
from threading import RLock
from weakref import WeakSet, ref

import numpy as np
from argdigest import arg_digest
from molsysviewer import AddonPanelWidget
from smonitor import signal

from ._panel_frontend import CSS, ESM

_DEFAULT = {
    "source": "none",
    "value": "",
    "expression": "",
    "indices": "",
    "context": "current",
    "structure_index": 0,
}
_CATEGORIES = {"water": "group_type=='water'", "ions": "group_type=='ion'"}
_SOURCES = {"none", "category", "current", "saved", "region", "expression", "indices"}


def _draft(value):
    if not isinstance(value, dict) or set(value) - set(_DEFAULT):
        raise ValueError("The selection draft contains unsupported fields.")
    result = dict(_DEFAULT, **value)
    if result["source"] not in _SOURCES or result["context"] not in {
        "current",
        "index",
    }:
        raise ValueError("Choose a supported selection source and structure context.")
    for key in ("value", "expression", "indices"):
        if not isinstance(result[key], str) or len(result[key]) > 4096:
            raise ValueError("Selection text must contain at most 4096 characters.")
    index = result["structure_index"]
    if isinstance(index, bool) or not isinstance(index, int) or index < 0:
        raise ValueError("The structure index must be a nonnegative integer.")
    return result


@dataclass
class _Review:
    token: str
    target: object
    revision: int
    structures: int
    frame: int
    draft: dict
    indices: np.ndarray
    groups: int | None


class _SystemPanel(AddonPanelWidget):
    _esm = ESM
    _css = CSS

    def __init__(self, view=None, **kwargs):
        super().__init__(view=view, **kwargs)
        self._owner = None
        self._alive = False
        self._review = None
        self._draft = dict(_DEFAULT)
        self._last_request = 0
        self._actions = RLock()

    @signal(tags=["addon", "panel"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def on_mount(self, view, *, skip_digestion=False):
        """Mounting the view-bound molecular task editor."""
        if view is not self._view or view.closed:
            raise ValueError("The panel requires its open owning view.")
        self._owner = view.addons.molsysmt
        self._alive = True
        try:
            self._draft = _draft(self.state.get("system_draft", {}))
        except (TypeError, ValueError):
            self._draft = dict(_DEFAULT)
        if not hasattr(self._owner, "_system_panels"):
            self._owner._system_panels = WeakSet()
        self._owner._system_panels.add(self)
        self._publish()

    @signal(tags=["addon", "panel"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def on_unmount(self, view, *, skip_digestion=False):
        """Discarding review tokens while leaving the bounded editor draft."""
        self._alive = False
        self._review = None
        if self._owner is not None:
            self._owner._system_panels.discard(self)
        self._owner = None

    def _context(self):
        view = self._view
        coordinator = getattr(view.addons.manager, "system_edits", None)
        if coordinator is None:
            return {
                "state": "unavailable",
                "has_system": view.molsys is not None,
                "can_review": False,
            }
        from molsysviewer.system_edits import SystemEditPendingError

        try:
            status = coordinator.get_status()
            context = {
                **status,
                "has_system": view.molsys is not None,
                "can_review": False,
            }
            if view.molsys is None:
                return context

            def read(target):
                saved = (
                    list(view.selections.tags())
                    if status["state"] == "synchronized"
                    else []
                )
                regions = (
                    list(view.regions.keys())
                    if status["state"] == "synchronized"
                    else []
                )
                return {
                    "n_atoms": int(target.get_n_atoms()),
                    "n_structures": int(target.structures.n_structures),
                    "structure_index": int(view.player.index),
                    "saved": saved[:200],
                    "regions": regions[:200],
                    "choices_truncated": len(saved) > 200 or len(regions) > 200,
                }

            if status["state"] in {"synchronized", "pending", "sync_failed"}:
                context.update(coordinator.read(read))
            context["can_review"] = (
                status["state"] == "synchronized" and context.get("n_structures", 0) > 0
            )
            return context

        except SystemEditPendingError:
            return {
                "state": "busy",
                "has_system": view.molsys is not None,
                "can_review": False,
            }

    def _publish(self, *, stage="select", message="", request_id=0):
        if not self._alive or self._view is None or self._view.closed:
            return
        context = self._context()
        review = self._review
        packet = {
            "request_id": request_id,
            "draft": dict(self._draft),
            "context": context,
            "stage": stage,
            "message": message,
        }
        if review is not None:
            packet["review"] = {
                "token": review.token,
                "remove_atoms": int(review.indices.size),
                "keep_atoms": context["n_atoms"] - int(review.indices.size),
                "n_structures": review.structures,
                "selection_structure": review.frame,
                "n_groups": review.groups,
            }
        if self._alive and self._view is not None and not self._view.closed:
            self.push_state(packet)

    def _selection(self, target, frame):
        from molsysmt import basic

        draft, view = self._draft, self._view
        source = draft["source"]
        if source == "category":
            if draft["value"] not in _CATEGORIES:
                raise ValueError("Choose Water or Ions.")
            selection = _CATEGORIES[draft["value"]]
        elif source == "current":
            selection = list(view.active_selection.atom_indices)
        elif source == "saved":
            item = view.selections.get(draft["value"])
            if item is None:
                raise ValueError(
                    "That saved selection no longer exists. Refresh the choices."
                )
            selection = list(item.atom_indices)
        elif source == "region":
            if draft["value"] not in view.regions:
                raise ValueError("That region no longer exists. Refresh the choices.")
            selection = list(view.regions[draft["value"]].atom_indices or ())
        elif source == "expression":
            selection = draft["expression"].strip()
            if not selection:
                raise ValueError("Enter a MolSysMT selection expression.")
        elif source == "indices":
            try:
                selection = [
                    int(word) for word in draft["indices"].replace(",", " ").split()
                ]
            except ValueError as exc:
                raise ValueError(
                    "Use comma- or space-separated integer atom indices."
                ) from exc
        else:
            raise ValueError("Choose which atoms to review.")
        # This is a native query with one explicit structure context, not a
        # per-structure topology edit or a consumer selection interpreter.
        return np.unique(
            np.asarray(
                basic.select(
                    target,
                    selection=selection,
                    structure_indices=[frame],
                    element="atom",
                    chemical_state="reference",
                ),
                dtype=np.int64,
            )
        )

    def _prepare_review(self, target):
        import pandas as pd

        from molsysmt import basic

        status = self._owner.get_sync_status()
        if status["state"] != "synchronized":
            raise ValueError("Update the view before reviewing a scene selection.")
        count = int(target.get_n_atoms())
        structures = int(target.structures.n_structures)
        frame = (
            int(self._view.player.index)
            if self._draft["context"] == "current"
            else self._draft["structure_index"]
        )
        if frame >= structures:
            raise ValueError("The selection structure index is outside this system.")
        indices = self._selection(target, frame)
        if indices.ndim != 1 or np.any(indices < 0) or np.any(indices >= count):
            raise ValueError("The selection contains atom indices outside this system.")
        if indices.size == count:
            raise ValueError(
                "This selects every atom. Choose a subset; clearing the view is a separate action."
            )
        if not indices.size:
            return None
        groups = basic.get(
            target, selection=indices.tolist(), element="atom", group_index=True
        )
        values = np.asarray(groups, dtype=object).reshape(-1)
        known = [int(i) for i in values if not pd.isna(i) and int(i) >= 0]
        n_groups = len(set(known)) if len(known) == indices.size else None
        indices = indices.copy()
        indices.setflags(write=False)
        return _Review(
            token_urlsafe(24),
            ref(target),
            status["target_revision"],
            structures,
            frame,
            dict(self._draft),
            indices,
            n_groups,
        )

    def _remove(self, token):
        review, self._review = self._review, None
        if review is None or token != review.token:
            raise ValueError("This review has expired. Review the selection again.")
        coordinator = self._view.addons.manager.system_edits

        def prepare(target):
            status = self._owner.get_sync_status()
            frame = (
                int(self._view.player.index)
                if self._draft["context"] == "current"
                else self._draft["structure_index"]
            )
            if (
                target is not review.target()
                or status["target_revision"] != review.revision
                or status["pending_operations"]
                or int(target.structures.n_structures) != review.structures
                or self._draft != review.draft
                or frame != review.frame
            ):
                raise ValueError(
                    "The system or selection context changed. Review the selection again."
                )
            if self._draft["source"] in {
                "current",
                "saved",
                "region",
            } and not np.array_equal(self._selection(target, frame), review.indices):
                raise ValueError(
                    "The selected atoms changed. Review the selection again."
                )
            # Reuse precisely the preparation adapter used by expert remove.
            # The precondition and native publication share one host lock.
            return self._owner.basic._prepare_removal(
                target,
                {
                    "selection": review.indices.tolist(),
                    "structure_indices": None,
                    "to_form": None,
                    "syntax": "MolSysMT",
                    "in_place": True,
                    "skip_digestion": False,
                },
            )

        coordinator.execute(prepare, name="molsysmt.basic.remove", update_view=True)
        for peer in list(self._owner._system_panels):
            if peer is not self and peer._alive:
                peer._review = None
                peer._publish(
                    message="The system changed in another window. Review the selection again."
                )

    @signal(tags=["addon", "panel"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def handle_action(self, view, action_id, payload, *, skip_digestion=False):
        """Handling one bounded editor request without changing the expert API."""
        if not self._alive or view is not self._view or view.closed:
            return
        with self._actions:
            request_id = (
                payload.get("request_id") if isinstance(payload, dict) else None
            )
            if (
                isinstance(request_id, bool)
                or not isinstance(request_id, int)
                or request_id <= self._last_request
            ):
                return
            self._last_request = request_id
            try:
                self._perform_action(action_id, payload, request_id)
            except Exception as exc:
                if not self._alive or self._owner is None or view.closed:
                    return
                self._review = None
                status = self._context()
                stage = (
                    "sync_required"
                    if getattr(exc, "science_completed", False)
                    and status["state"] in {"pending", "sync_failed"}
                    else "recovery_required"
                    if status["state"] == "uncertain"
                    else "error"
                )
                message = (
                    "The molecular edit completed. Retry only the view update."
                    if stage == "sync_required"
                    else "The system needs explicit recovery before further editing."
                    if stage == "recovery_required"
                    else str(exc)[:1000]
                )
                self._publish(stage=stage, message=message, request_id=request_id)

    @signal(tags=["addon", "panel"], exception_level="DEBUG")
    def _perform_action(self, action_id, payload, request_id):
        if set(payload) - {"request_id", "draft", "token"}:
            raise ValueError("The panel request contains unsupported fields.")
        if "draft" in payload:
            draft = _draft(payload["draft"])
            if draft != self._draft:
                self._review = None
            self._draft = draft
            self.set_state({"system_draft": dict(draft)})
        if action_id == "refresh":
            self._review = None
            self._publish(request_id=request_id)
            return
        if action_id not in {"review", "remove", "back"}:
            raise ValueError("This molecular task is not available.")
        if action_id == "back":
            self._review = None
            self._publish(request_id=request_id)
        elif action_id == "review":
            self._review = None
            self._review = self._owner._read(
                lambda target: self._prepare_review(target), {}
            )
            self._publish(
                stage="review" if self._review is not None else "no_matches",
                message=""
                if self._review is not None
                else "Nothing to remove: no atoms match this selection.",
                request_id=request_id,
            )
        else:
            self._remove(payload.get("token"))
            self._publish(
                stage="done",
                message="Selected atoms removed. The view is up to date.",
                request_id=request_id,
            )
