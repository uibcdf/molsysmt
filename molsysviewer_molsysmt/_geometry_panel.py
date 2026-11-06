"""Explicit translation task over the qualified native geometry adapter."""

from dataclasses import dataclass
from secrets import token_urlsafe
from weakref import ref

import numpy as np
from smonitor import signal

from ._geometry import _geometry_token, _prepare_geometry_transform
from ._geometry_panel_frontend import ESM
from ._panel_frontend import CSS
from ._task_panel import _MolecularTaskPanel, _structures

_PARAMETERS = {
    "dx": "0",
    "dy": "0",
    "dz": "0",
    "unit": "angstrom",
    "structures": "all",
    "indices": "",
    "effect": "update",
    "title": "",
}
_COMPLETED = "Translation applied. The view is up to date."


def _parameters(value):
    if not isinstance(value, dict) or set(value) - set(_PARAMETERS):
        raise ValueError("The translation contains unsupported fields.")
    result = dict(_PARAMETERS, **value)
    if result["unit"] not in {"angstrom", "nm"} or result["effect"] not in {
        "update",
        "result",
    }:
        raise ValueError("Choose a length unit and the translation destination.")
    if result["structures"] not in {"all", "current", "indices"}:
        raise ValueError("Choose which structures to translate.")
    for key, limit in (
        ("dx", 64),
        ("dy", 64),
        ("dz", 64),
        ("indices", 4096),
        ("title", 200),
    ):
        if not isinstance(result[key], str) or len(result[key]) > limit:
            raise ValueError("Translation fields contain invalid or overlong text.")
    return result


def _translation(parameters):
    from molsysmt import pyunitwizard as puw

    try:
        values = [float(parameters[key]) for key in ("dx", "dy", "dz")]
    except ValueError as exc:
        raise ValueError("Enter three finite displacement values.") from exc
    if not np.all(np.isfinite(values)):
        raise ValueError("Enter three finite displacement values.")
    # The GUI record carries its explicit unit. Native digestion still owns
    # dimensional validation and supported coordinate broadcasting.
    return puw.quantity(values, parameters["unit"])


@dataclass(frozen=True)
class _TranslationReview:
    token: str
    target: object
    revision: int
    structures: int
    frame: int
    draft: dict
    parameters: dict
    indices: np.ndarray
    frames: tuple


class _GeometryPanel(_MolecularTaskPanel):
    _esm = ESM
    _css = CSS
    _state_key = "geometry_selection"
    _allow_all = True

    def __init__(self, view=None, **kwargs):
        super().__init__(view=view, **kwargs)
        self._parameters = dict(_PARAMETERS)

    def _restore_inputs(self):
        try:
            self._parameters = _parameters(self.state.get("translation_parameters", {}))
        except (TypeError, ValueError):
            self._parameters = dict(_PARAMETERS)

    def _publish(self, *, stage="select", message="", request_id=0):
        if not self._alive or self._view is None or self._view.closed:
            return
        context = self._context()
        self._refresh_result()
        if self._outcome is not None:
            target, revision, draft, parameters = self._outcome
            if (
                self._view.molsys is target()
                and context.get("state") == "synchronized"
                and context.get("target_revision") == revision
                and draft == self._draft
                and parameters == self._parameters
            ):
                if stage == "select" and not message:
                    stage, message = "done", _COMPLETED
            else:
                self._outcome = None
        service = getattr(self._view.addons.manager, "presentations", None)
        packet = {
            "request_id": request_id,
            "draft": dict(self._draft),
            "parameters": dict(self._parameters),
            "context": context,
            "stage": stage,
            "message": message,
            "result": self._result,
            "destinations": list(getattr(service, "destinations", ())),
        }
        if self._review is not None:
            review = self._review
            packet["review"] = {
                "token": review.token,
                "n_atoms": int(review.indices.size),
                "n_structures": len(review.frames),
                "selection_structure": review.frame,
                "structure_indices": list(review.frames[:200]),
                "structures_truncated": len(review.frames) > 200,
            }
        self.push_state(packet)

    def _resolve(self, target):
        status = self._owner.get_sync_status()
        if status["state"] != "synchronized" and status["state"] != "editing":
            raise ValueError("Update the view before reviewing molecular coordinates.")
        if target.structures.coordinates is None:
            raise ValueError("Load coordinates before translating a molecular system.")
        total = int(target.structures.n_structures)
        frame = (
            int(self._view.player.index)
            if self._draft["context"] == "current"
            else self._draft["structure_index"]
        )
        if frame >= total:
            raise ValueError("The selection structure index is outside this system.")
        atoms = self._selection(target, frame)
        if (
            atoms.ndim != 1
            or np.any(atoms < 0)
            or np.any(atoms >= int(target.get_n_atoms()))
        ):
            raise ValueError("The selection contains atom indices outside this system.")
        frames = _structures(
            self._parameters["structures"],
            self._parameters["indices"],
            total,
            int(self._view.player.index),
        )
        _translation(self._parameters)
        return status, total, frame, atoms, tuple(frames)

    def _prepare_review(self, target):
        status, total, frame, atoms, frames = self._resolve(target)
        if not atoms.size:
            return None
        atoms = atoms.copy()
        atoms.setflags(write=False)
        return _TranslationReview(
            token_urlsafe(24),
            ref(target),
            status["target_revision"],
            total,
            frame,
            dict(self._draft),
            dict(self._parameters),
            atoms,
            frames,
        )

    def _check_review(self, target, review):
        status = self._owner.get_sync_status()
        if (
            target is not review.target()
            or status["target_revision"] != review.revision
            or status["pending_operations"]
            or self._draft != review.draft
            or self._parameters != review.parameters
        ):
            raise ValueError(
                "The system or translation changed. Review the translation again."
            )
        _, total, frame, atoms, frames = self._resolve(target)
        if (
            total != review.structures
            or frame != review.frame
            or frames != review.frames
            or not np.array_equal(atoms, review.indices)
        ):
            raise ValueError(
                "The selected atoms or structures changed. Review the translation again."
            )
        return {
            "translation": _translation(review.parameters),
            "selection": atoms.tolist(),
            "structure_indices": list(frames),
            "syntax": "MolSysMT",
            "in_place": True,
            "skip_digestion": False,
        }

    def _apply(self, token):
        review, self._review = self._review, None
        if review is None or token != review.token:
            raise ValueError("This review has expired. Review the translation again.")
        if review.parameters["effect"] == "update":

            def prepare(target):
                return _prepare_geometry_transform(
                    target, "translate", self._check_review(target, review)
                )

            self._view.addons.manager.system_edits.execute(
                prepare,
                name="molsysmt.structure.translate",
                update_view=True,
                rejection_check=_geometry_token,
            )
            self._outcome = (
                review.target,
                review.revision + 1,
                dict(review.draft),
                dict(review.parameters),
            )
            self._invalidate_peers()
        else:
            if self._result is not None:
                raise ValueError(
                    "Close or leave the previous result before calculating another."
                )

            def calculate(target):
                parameters = self._check_review(target, review)
                parameters["in_place"] = False
                candidate = self._owner.structure.translate(**parameters)
                result = self._store_result(
                    candidate,
                    title=review.parameters["title"].strip() or "Translated system",
                    operation="molsysmt.structure.translate",
                    structure_indices=list(range(review.structures)),
                    revision=review.revision,
                )
                result["affected_structures"] = list(review.frames[:200])
                result["affected_truncated"] = len(review.frames) > 200
                return result

            self._result = self._owner._read(calculate, {})

    @signal(tags=["addon", "panel"], exception_level="DEBUG")
    def _perform_action(self, action_id, payload, request_id):
        if set(payload) - {"request_id", "draft", "parameters", "token"}:
            raise ValueError("The geometry request contains unsupported fields.")
        draft = self._normalize_draft(payload.get("draft", self._draft))
        parameters = _parameters(payload.get("parameters", self._parameters))
        if draft != self._draft or parameters != self._parameters:
            self._review = None
            self._outcome = None
        self._draft, self._parameters = draft, parameters
        self.set_state(
            {self._state_key: dict(draft), "translation_parameters": dict(parameters)}
        )
        if action_id in {"refresh", "back"}:
            self._review = None
        elif action_id == "review":
            self._outcome = None
            self._review = None
            self._review = self._owner._read(self._prepare_review, {})
            self._publish(
                stage="review" if self._review else "no_matches",
                message=""
                if self._review
                else "Nothing to translate: no atoms match this selection.",
                request_id=request_id,
            )
            return
        elif action_id == "apply":
            self._outcome = None
            self._apply(payload.get("token"))
            self._publish(
                stage="result" if self._result else "done",
                message="" if self._result else _COMPLETED,
                request_id=request_id,
            )
            return
        elif action_id == "result.new":
            self._discard_unpresented_result()
        elif action_id == "result.discard":
            if self._result is not None:
                self._view.addons.manager.presentations.close(self._result["id"])
                self._result = None
        else:
            raise ValueError("This Geometry task is unavailable.")
        self._publish(request_id=request_id)
