"""Reviewed translation and centering over qualified native geometry adapters."""

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
    "task": "translate",
    "cx": "0",
    "cy": "0",
    "cz": "0",
    "center_unit": "angstrom",
    "center_kind": "geometric",
    "source_expression": "",
    "destination_kind": "point",
    "target_expression": "",
    "dx": "0",
    "dy": "0",
    "dz": "0",
    "unit": "angstrom",
    "structures": "all",
    "indices": "",
    "effect": "update",
    "title": "",
}
_COMPLETED = {
    "translate": "Translation applied. The view is up to date.",
    "center": "Centering applied. The view is up to date.",
}


def _parameters(value):
    if not isinstance(value, dict) or set(value) - set(_PARAMETERS):
        raise ValueError("The coordinate request contains unsupported fields.")
    result = dict(_PARAMETERS, **value)
    if result["task"] not in {"translate", "center"}:
        raise ValueError("Choose a supported Geometry task.")
    if result["center_kind"] not in {"geometric", "masses"} or result[
        "destination_kind"
    ] not in {"point", "selection"}:
        raise ValueError("Choose a supported center and destination.")
    if result["center_unit"] not in {"angstrom", "nm"}:
        raise ValueError("Choose an explicit center length unit.")
    if result["unit"] not in {"angstrom", "nm"} or result["effect"] not in {
        "update",
        "result",
    }:
        raise ValueError("Choose a length unit and the result destination.")
    if result["structures"] not in {"all", "current", "indices"}:
        raise ValueError("Choose which structures to translate.")
    for key, limit in (
        ("dx", 64),
        ("dy", 64),
        ("dz", 64),
        ("cx", 64),
        ("cy", 64),
        ("cz", 64),
        ("source_expression", 4096),
        ("target_expression", 4096),
        ("indices", 4096),
        ("title", 200),
    ):
        if not isinstance(result[key], str) or len(result[key]) > limit:
            raise ValueError("Coordinate fields contain invalid or overlong text.")
    return result


def _translation(parameters, *, center=False):
    from molsysmt import pyunitwizard as puw

    try:
        values = [
            float(parameters[key])
            for key in (("cx", "cy", "cz") if center else ("dx", "dy", "dz"))
        ]
    except ValueError as exc:
        raise ValueError("Enter three finite length values.") from exc
    if not np.all(np.isfinite(values)):
        raise ValueError("Enter three finite length values.")
    # The GUI record carries its explicit unit. Native digestion still owns
    # dimensional validation and supported coordinate broadcasting.
    return puw.quantity(values, parameters["center_unit" if center else "unit"])


@dataclass(frozen=True)
class _GeometryReview:
    token: str
    target: object
    revision: int
    structures: int
    frame: int
    draft: dict
    parameters: dict
    indices: np.ndarray
    frames: tuple
    center_indices: tuple
    target_indices: tuple


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

    def _diagnostic_inputs(self):
        return (dict(self._draft), dict(self._parameters))

    def _publish(self, *, stage="select", message="", request_id=0):
        if not self._alive or self._view is None or self._view.closed:
            return
        context = self._context()
        self._refresh_result()
        stage, message = self._retained_diagnostic(context, stage, message)
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
                    stage, message = "done", _COMPLETED[self._parameters["task"]]
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
                "n_center_atoms": len(review.center_indices),
                "n_target_atoms": len(review.target_indices),
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
            raise ValueError("Load coordinates before transforming a molecular system.")
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
        center_indices, target_indices = (), ()
        if self._parameters["task"] == "translate":
            _translation(self._parameters)
        else:
            from molsysmt import basic

            def population(expression, fallback):
                if not expression.strip():
                    return tuple(int(i) for i in fallback)
                indices = np.asarray(
                    basic.select(
                        target,
                        selection=expression.strip(),
                        element="atom",
                        structure_indices=[frame],
                        chemical_state="reference",
                    ),
                    dtype=np.int64,
                )
                if indices.ndim != 1 or not indices.size:
                    raise ValueError(
                        "A center expression must select a nonempty atom population."
                    )
                return tuple(int(i) for i in np.unique(indices))

            center_indices = population(self._parameters["source_expression"], atoms)
            moving_set = set(atoms.tolist())
            if not all(i in moving_set for i in center_indices):
                raise ValueError(
                    "Source center atoms must belong to the moving selection."
                )
            if self._parameters["destination_kind"] == "point":
                _translation(self._parameters, center=True)
            else:
                if not self._parameters["target_expression"].strip():
                    raise ValueError("Choose a target-center selection expression.")
                target_indices = population(self._parameters["target_expression"], ())
        return (
            status,
            total,
            frame,
            atoms,
            tuple(frames),
            center_indices,
            target_indices,
        )

    def _prepare_review(self, target):
        status, total, frame, atoms, frames, centers, targets = self._resolve(target)
        if not atoms.size:
            return None
        atoms = atoms.copy()
        atoms.setflags(write=False)
        return _GeometryReview(
            token_urlsafe(24),
            ref(target),
            status["target_revision"],
            total,
            frame,
            dict(self._draft),
            dict(self._parameters),
            atoms,
            frames,
            centers,
            targets,
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
                "The system or requested coordinate change changed. Review the coordinate change again."
            )
        _, total, frame, atoms, frames, centers, targets = self._resolve(target)
        if (
            total != review.structures
            or frame != review.frame
            or frames != review.frames
            or centers != review.center_indices
            or targets != review.target_indices
            or not np.array_equal(atoms, review.indices)
        ):
            raise ValueError(
                "The selected atoms or structures changed. Review the coordinate change again."
            )
        parameters = {
            "selection": atoms.tolist(),
            "structure_indices": list(frames),
            "syntax": "MolSysMT",
            "in_place": True,
            "skip_digestion": False,
        }
        if review.parameters["task"] == "translate":
            parameters["translation"] = _translation(review.parameters)
        else:
            parameters.update(
                {
                    "source_center_selection": list(centers),
                    "target_center_selection": list(targets) if targets else None,
                    "target_coordinates": None
                    if targets
                    else _translation(review.parameters, center=True),
                    "weights": None
                    if review.parameters["center_kind"] == "geometric"
                    else "masses",
                    "engine": "MolSysMT",
                }
            )
        return parameters

    def _apply(self, token):
        review, self._review = self._review, None
        if review is None or token != review.token:
            raise ValueError(
                "This review has expired. Review the coordinate change again."
            )
        if review.parameters["effect"] == "update":

            def prepare(target):
                return _prepare_geometry_transform(
                    target,
                    review.parameters["task"],
                    self._check_review(target, review),
                )

            self._view.addons.manager.system_edits.execute(
                prepare,
                name="molsysmt.structure." + review.parameters["task"],
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
                operation = getattr(self._owner.structure, review.parameters["task"])
                candidate = operation(**parameters)
                result = self._store_result(
                    candidate,
                    title=review.parameters["title"].strip()
                    or (
                        "Translated system"
                        if review.parameters["task"] == "translate"
                        else "Centered system"
                    ),
                    operation="molsysmt.structure." + review.parameters["task"],
                    structure_indices=list(range(review.structures)),
                    revision=review.revision,
                )
                result["effect_label"] = (
                    "Translated"
                    if review.parameters["task"] == "translate"
                    else "Centered"
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
        if action_id in {"refresh", "back", "task"}:
            self._review = None
            if action_id == "task":
                self._discard_unpresented_result()
                self._outcome = None
        elif action_id == "review":
            self._outcome = None
            self._review = None
            self._review = self._owner._read(self._prepare_review, {})
            self._publish(
                stage="review" if self._review else "no_matches",
                message=""
                if self._review
                else "Nothing to transform: no atoms match this selection.",
                request_id=request_id,
            )
            return
        elif action_id == "apply":
            self._outcome = None
            self._apply(payload.get("token"))
            self._publish(
                stage="result" if self._result else "done",
                message="" if self._result else _COMPLETED[self._parameters["task"]],
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
