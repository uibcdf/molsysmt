"""Reviewed coordinate tasks over qualified native geometry adapters."""

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
    "wrap_mode": "primary",
    "wrap_compact": "component",
    "ox": "0",
    "oy": "0",
    "oz": "0",
    "origin_unit": "angstrom",
    "fit_expression": "",
    "fit_reference_expression": "",
    "fit_reference_structure": "0",
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
    "fit": "Superposition applied. The view is up to date.",
    "wrap": "Periodic wrapping applied. The view is up to date.",
    "unwrap": "Temporal unwrapping applied. The view is up to date.",
}

_OPERATIONS = {
    "translate": ("structure", "translate"),
    "center": ("structure", "center"),
    "fit": ("structure", "least_rmsd_fit"),
    "wrap": ("pbc", "wrap_to_pbc"),
    "unwrap": ("pbc", "unwrap"),
}


def _operation(parameters):
    module, name = _OPERATIONS[parameters["task"]]
    if parameters["task"] == "wrap" and parameters["wrap_mode"] == "nearest":
        name = "wrap_to_mic"
    return module, name


_RESULT_TITLES = {
    "translate": "Translated system",
    "center": "Centered system",
    "fit": "Superposed system",
    "wrap": "Wrapped system",
    "unwrap": "Unwrapped trajectory",
}
_EFFECT_LABELS = {
    "translate": "Translated",
    "center": "Centered",
    "fit": "Superposed",
    "wrap": "Wrapped",
    "unwrap": "Unwrapped",
}


def _parameters(value):
    if not isinstance(value, dict) or set(value) - set(_PARAMETERS):
        raise ValueError("The coordinate request contains unsupported fields.")
    result = dict(_PARAMETERS, **value)
    if result["task"] not in _OPERATIONS:
        raise ValueError("Choose a supported Geometry task.")
    if result["wrap_mode"] not in {"primary", "centered", "nearest"} or result[
        "wrap_compact"
    ] not in {"component", "atom"}:
        raise ValueError("Choose a supported periodic placement and grouping.")
    if result["origin_unit"] not in {"angstrom", "nm"}:
        raise ValueError("Choose an explicit periodic reference length unit.")
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
        raise ValueError("Choose which structures to transform.")
    for key, limit in (
        ("ox", 64),
        ("oy", 64),
        ("oz", 64),
        ("dx", 64),
        ("dy", 64),
        ("dz", 64),
        ("cx", 64),
        ("cy", 64),
        ("cz", 64),
        ("source_expression", 4096),
        ("fit_expression", 4096),
        ("fit_reference_expression", 4096),
        ("fit_reference_structure", 64),
        ("target_expression", 4096),
        ("indices", 4096),
        ("title", 200),
    ):
        if not isinstance(result[key], str) or len(result[key]) > limit:
            raise ValueError("Coordinate fields contain invalid or overlong text.")
    return result


def _length_vector(parameters, kind="translation"):
    from molsysmt import pyunitwizard as puw

    fields, unit = {
        "translation": (("dx", "dy", "dz"), "unit"),
        "center": (("cx", "cy", "cz"), "center_unit"),
        "origin": (("ox", "oy", "oz"), "origin_unit"),
    }[kind]
    try:
        values = [float(parameters[key]) for key in fields]
    except ValueError as exc:
        raise ValueError("Enter three finite length values.") from exc
    if not np.all(np.isfinite(values)):
        raise ValueError("Enter three finite length values.")
    return puw.quantity(values, parameters[unit])


def _admit_periodic_profile(target, frames, *, temporal):
    """Bound the GUI's received native route; never repair a box or an image."""
    from molsysmt import basic
    from molsysmt import pyunitwizard as puw

    box = basic.get(target, structure_indices=list(frames), box=True)
    if box is None:
        raise ValueError(
            "Periodic tools require stored box vectors. Load box data or explicitly assign a box before using this task."
        )
    values = np.asarray(puw.get_value(box, to_unit="nm"))
    # Temporary input admission for owner #607, not a new physical definition.
    # No tolerance, rotation or minimum-image algorithm is introduced here.
    if np.any(np.triu(values, k=1) != 0):
        raise ValueError(
            "This periodic editor does not yet support that box orientation. The molecular data were not changed."
        )
    if temporal and not np.all(values == values[:1]):
        raise ValueError(
            "Temporal unwrapping currently requires an unchanged periodic cell across the selected structures. Changing-cell support is pending."
        )


@dataclass(frozen=True)
class _GeometryReferences:
    center: tuple = ()
    target: tuple = ()
    fit: tuple = ()
    reference: tuple = ()
    reference_frame: int | None = None


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
    references: _GeometryReferences


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
                "n_center_atoms": len(review.references.center),
                "n_target_atoms": len(review.references.target),
                "n_fit_atoms": len(review.references.fit),
                "reference_structure": review.references.reference_frame,
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
        from molsysmt import basic

        def population(expression, fallback, context_frame=frame):
            if not expression.strip():
                return tuple(int(i) for i in fallback)
            indices = np.asarray(
                basic.select(
                    target,
                    selection=expression.strip(),
                    element="atom",
                    structure_indices=[context_frame],
                    chemical_state="reference",
                ),
                dtype=np.int64,
            )
            if indices.ndim != 1 or not indices.size:
                raise ValueError(
                    "A reference expression must select a nonempty atom population."
                )
            return tuple(int(i) for i in np.unique(indices))

        references = _GeometryReferences()
        if self._parameters["task"] == "translate":
            _length_vector(self._parameters)
        elif self._parameters["task"] in {"wrap", "unwrap"}:
            temporal = self._parameters["task"] == "unwrap"
            if temporal and len(frames) < 2:
                raise ValueError(
                    "Choose at least two structures in their intended temporal order."
                )
            if atoms.size:
                _admit_periodic_profile(target, frames, temporal=temporal)
            if not temporal:
                _length_vector(self._parameters, "origin")
        elif self._parameters["task"] == "center":
            centers = population(self._parameters["source_expression"], atoms)
            moving_set = set(atoms.tolist())
            if not all(i in moving_set for i in centers):
                raise ValueError(
                    "Source center atoms must belong to the moving selection."
                )
            targets = ()
            if self._parameters["destination_kind"] == "point":
                _length_vector(self._parameters, "center")
            else:
                if not self._parameters["target_expression"].strip():
                    raise ValueError("Choose a target-center selection expression.")
                targets = population(self._parameters["target_expression"], ())
            references = _GeometryReferences(center=centers, target=targets)
        else:
            text = self._parameters["fit_reference_structure"].strip()
            try:
                reference_frame = int(text)
            except ValueError as exc:
                raise ValueError(
                    "Choose an integer reference structure index."
                ) from exc
            if not 0 <= reference_frame < total:
                raise ValueError(
                    "The reference structure index is outside this system."
                )
            fit = population(self._parameters["fit_expression"], atoms)
            reference = population(
                self._parameters["fit_reference_expression"], fit, reference_frame
            )
            if atoms.size and (len(fit) < 3 or len(reference) != len(fit)):
                raise ValueError(
                    "A rigid fit needs at least three corresponding atom pairs with equal population sizes."
                )
            references = _GeometryReferences(
                fit=fit, reference=reference, reference_frame=reference_frame
            )
        return status, total, frame, atoms, tuple(frames), references

    def _prepare_review(self, target):
        status, total, frame, atoms, frames, references = self._resolve(target)
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
            references,
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
        _, total, frame, atoms, frames, references = self._resolve(target)
        if (
            total != review.structures
            or frame != review.frame
            or frames != review.frames
            or references != review.references
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
            parameters["translation"] = _length_vector(review.parameters)
        elif review.parameters["task"] in {"wrap", "unwrap"}:
            parameters["engine"] = "MolSysMT"
            if review.parameters["task"] == "wrap":
                parameters["compact"] = (
                    "component"
                    if review.parameters["wrap_compact"] == "component"
                    else False
                )
                field = {
                    "primary": "box_origin",
                    "centered": "box_center",
                    "nearest": "mic_origin",
                }[review.parameters["wrap_mode"]]
                parameters[field] = _length_vector(review.parameters, "origin")
        elif review.parameters["task"] == "center":
            parameters.update(
                {
                    "source_center_selection": list(references.center),
                    "target_center_selection": list(references.target)
                    if references.target
                    else None,
                    "target_coordinates": None
                    if references.target
                    else _length_vector(review.parameters, "center"),
                    "weights": None
                    if review.parameters["center_kind"] == "geometric"
                    else "masses",
                    "engine": "MolSysMT",
                }
            )
        else:
            parameters.update(
                {
                    "selection_fit": list(references.fit),
                    "reference_molecular_system": None,
                    "reference_selection_fit": list(references.reference),
                    "reference_structure_index": references.reference_frame,
                    "engine": "MolSysMT",
                    "use_gpu": False,
                }
            )
        return parameters

    def _apply(self, token):
        review, self._review = self._review, None
        if review is None or token != review.token:
            raise ValueError(
                "This review has expired. Review the coordinate change again."
            )
        module, name = _operation(review.parameters)
        if review.parameters["effect"] == "update":

            def prepare(target):
                return _prepare_geometry_transform(
                    target,
                    name,
                    self._check_review(target, review),
                    module=module,
                )

            self._view.addons.manager.system_edits.execute(
                prepare,
                name=f"molsysmt.{module}.{name}",
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
                operation = getattr(getattr(self._owner, module), name)
                candidate = operation(**parameters)
                result = self._store_result(
                    candidate,
                    title=review.parameters["title"].strip()
                    or _RESULT_TITLES[review.parameters["task"]],
                    operation=f"molsysmt.{module}.{name}",
                    structure_indices=list(range(review.structures)),
                    revision=review.revision,
                )
                result["effect_label"] = _EFFECT_LABELS[review.parameters["task"]]
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
