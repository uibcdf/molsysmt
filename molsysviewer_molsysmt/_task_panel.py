"""Shared selection, lifecycle and result ownership for molecular task panels."""

from copy import deepcopy
from dataclasses import dataclass
from threading import RLock
from weakref import WeakSet, ref

import numpy as np
from argdigest import arg_digest
from molsysviewer import AddonPanelWidget
from smonitor import signal

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


def _draft(value, *, allow_all=False):
    if not isinstance(value, dict) or set(value) - set(_DEFAULT):
        raise ValueError("The selection draft contains unsupported fields.")
    result = dict(_DEFAULT, **value)
    if result["source"] not in (_SOURCES | ({"all"} if allow_all else set())) or result[
        "context"
    ] not in {
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


def _structures(scope, text, total, current):
    if scope == "all":
        indices = list(range(total))
    elif scope == "current":
        indices = [current]
    elif scope == "indices":
        try:
            indices = [int(word) for word in text.replace(",", " ").split()]
        except ValueError as exc:
            raise ValueError(
                "Use integer structure indices in the desired order."
            ) from exc
    else:
        raise ValueError("Choose All, Current or explicit structure indices.")
    if (
        not indices
        or len(set(indices)) != len(indices)
        or any(i < 0 or i >= total for i in indices)
    ):
        raise ValueError(
            "Choose nonempty, distinct structure indices within this system."
        )
    return indices


@dataclass(frozen=True)
class _TaskDiagnostic:
    target: object
    revision: int | None
    state: str
    frame: int | None
    inputs: tuple
    stage: str
    message: str


class _MolecularTaskPanel(AddonPanelWidget):
    _state_key = "system_draft"
    _allow_all = False

    def __init__(self, view=None, **kwargs):
        super().__init__(view=view, **kwargs)
        self._owner = None
        self._alive = False
        self._review = None
        self._outcome = None
        self._diagnostic = None
        self._draft = dict(_DEFAULT)
        self._last_request = 0
        self._actions = RLock()
        self._result = None

    def _normalize_draft(self, value):
        return _draft(value, allow_all=self._allow_all)

    def _restore_inputs(self):
        pass

    def _release_task_data(self):
        """Release panel-owned reports when their mounted lifetime ends."""

    @signal(tags=["addon", "panel"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def on_mount(self, view, *, skip_digestion=False):
        """Mounting the view-bound molecular task editor."""
        if view is not self._view or view.closed:
            raise ValueError("The panel requires its open owning view.")
        self._owner = view.addons.molsysmt
        self._alive = True
        self._outcome = None
        self._diagnostic = None
        try:
            self._draft = self._normalize_draft(self.state.get(self._state_key, {}))
        except (TypeError, ValueError):
            self._draft = dict(_DEFAULT)
        if not hasattr(self._owner, "_task_panels"):
            self._owner._task_panels = WeakSet()
        self._owner._task_panels.add(self)
        self._restore_inputs()
        self._publish()

    @signal(tags=["addon", "panel"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def on_unmount(self, view, *, skip_digestion=False):
        """Discarding review tokens while leaving the bounded editor draft."""
        self._alive = False
        self._review = None
        self._outcome = None
        self._diagnostic = None
        self._release_task_data()
        if self._owner is not None:
            self._owner._task_panels.discard(self)
        self._owner = None
        self._discard_unpresented_result()

    def _discard_unpresented_result(self):
        if self._result is not None:
            service = self._view.addons.manager.presentations
            records = {item["id"]: item for item in service.records()}
            record = records.get(self._result["id"])
            if record is not None and record["destination"] is None:
                service.close(self._result["id"])
            self._result = None

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

    def _diagnostic_inputs(self):
        return (dict(self._draft),)

    def _retained_diagnostic(self, context, stage, message):
        diagnostic = self._diagnostic
        if diagnostic is not None:
            if (
                self._view.molsys
                is not (diagnostic.target() if diagnostic.target else None)
                or context.get("target_revision") != diagnostic.revision
                or context.get("state") != diagnostic.state
                or context.get("structure_index") != diagnostic.frame
                or self._diagnostic_inputs() != diagnostic.inputs
            ):
                self._diagnostic = None
            elif stage == "select" and not message:
                stage, message = diagnostic.stage, diagnostic.message
        return stage, message

    def _refresh_result(self):
        if self._result is not None:
            records = self._view.addons.manager.presentations.records()
            if not any(record["id"] == self._result["id"] for record in records):
                self._result = None

    def _selection(self, target, frame, *, unique=True):
        from molsysmt import basic

        draft, view = self._draft, self._view
        source = draft["source"]
        if source == "all" and self._allow_all:
            selection = "all"
        elif source == "category":
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
        indices = np.asarray(
            basic.select(
                target,
                selection=selection,
                structure_indices="all" if frame is None else [frame],
                element="atom",
                chemical_state="reference",
            ),
            dtype=np.int64,
        )
        return np.unique(indices) if unique else indices

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
            if action_id != "refresh":
                self._diagnostic = None
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
                # Store only bounded display data, never an exception, molecular
                # arrays or a confirmation token. Automatic refresh is a context
                # read, not permission to erase the rejected operation's outcome.
                self._diagnostic = _TaskDiagnostic(
                    ref(view.molsys) if view.molsys is not None else None,
                    status.get("target_revision"),
                    status["state"],
                    status.get("structure_index"),
                    deepcopy(self._diagnostic_inputs()),
                    stage,
                    message,
                )
                self._publish(stage=stage, message=message, request_id=request_id)

    def _invalidate_peers(self):
        for peer in list(self._owner._task_panels):
            if peer is not self and peer._alive:
                peer._review = None
                peer._publish(
                    message="The system changed in another window. Review the selection again."
                )

    def _store_result(
        self, candidate, *, title, operation, structure_indices, revision
    ):
        import molsysviewer as msv

        service = getattr(self._view.addons.manager, "presentations", None)
        if (
            service is None
            or not callable(getattr(service, "prepare", None))
            or not service.destinations
        ):
            raise RuntimeError(
                "Update the Viewer host to present independent molecular results."
            )
        metadata = {
            "title": title,
            "n_atoms": int(candidate.get_n_atoms()),
            "n_structures": int(candidate.structures.n_structures),
            "structure_indices": structure_indices[:200],
            "structures_truncated": len(structure_indices) > 200,
            "operation": operation,
            "source_revision": revision,
        }
        handle = service.prepare(
            lambda child: msv.new_view(candidate, view=child), title=title
        )
        return {"id": handle, **metadata}
