"""Reviewed coordinate tasks over qualified native geometry adapters."""

from dataclasses import dataclass
from pathlib import Path
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
    "axes_expression": "",
    "axes_type": "inertia",
    "axes_weights": "uniform",
    "axes_center": "preserve",
    "axes_target": "cartesian",
    "axes_basis": "1 0 0; 0 1 0; 0 0 1",
    "ax": "0",
    "ay": "0",
    "az": "1",
    "angle": "90",
    "angle_unit": "degree",
    "rotation_center_kind": "geometric",
    "wrap_mode": "primary",
    "wrap_compact": "component",
    "ox": "0",
    "oy": "0",
    "oz": "0",
    "origin_unit": "angstrom",
    "fit_expression": "",
    "fit_reference_expression": "",
    "fit_reference_structure": "0",
    "fit_reference_kind": "system",
    "fit_reference_filename": "",
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
    "axes": "Principal-axis alignment applied. The view is up to date.",
    "translate": "Translation applied. The view is up to date.",
    "rotate": "Rotation applied. The view is up to date.",
    "center": "Centering applied. The view is up to date.",
    "fit": "Superposition applied. The view is up to date.",
    "wrap": "Periodic wrapping applied. The view is up to date.",
    "unwrap": "Temporal unwrapping applied. The view is up to date.",
}

_OPERATIONS = {
    "axes": ("structure", "align_principal_axes"),
    "translate": ("structure", "translate"),
    "rotate": ("structure", "rotate"),
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
    "axes": "Principal-axis aligned system",
    "translate": "Translated system",
    "rotate": "Rotated system",
    "center": "Centered system",
    "fit": "Superposed system",
    "wrap": "Wrapped system",
    "unwrap": "Unwrapped trajectory",
}
_EFFECT_LABELS = {
    "axes": "Aligned",
    "translate": "Translated",
    "rotate": "Rotated",
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
    if (
        result["axes_type"] not in {"inertia", "geometric"}
        or result["axes_weights"] not in {"uniform", "masses"}
        or result["axes_center"] not in {"preserve", "origin"}
        or result["axes_target"] not in {"cartesian", "custom"}
    ):
        raise ValueError(
            "Choose supported principal-axis, weighting and target options."
        )
    if result["angle_unit"] not in {"degree", "radian"} or result[
        "rotation_center_kind"
    ] not in {"geometric", "origin", "point"}:
        raise ValueError("Choose an explicit angle unit and rotation center.")
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
    if result["fit_reference_kind"] not in {"system", "file"}:
        raise ValueError("Choose the current system or an external reference file.")
    for key, limit in (
        ("axes_expression", 4096),
        ("axes_basis", 512),
        ("ax", 64),
        ("ay", 64),
        ("az", 64),
        ("angle", 64),
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
        ("fit_reference_filename", 4096),
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


def _rotation(parameters):
    from molsysmt import pyunitwizard as puw
    from molsysmt.structure import get_rotation_matrix_from_axis_angle

    try:
        axis = [float(parameters[key]) for key in ("ax", "ay", "az")]
        angle = float(parameters["angle"])
    except ValueError as exc:
        raise ValueError("Enter a finite nonzero axis and a finite angle.") from exc
    return get_rotation_matrix_from_axis_angle(
        axis, puw.quantity(angle, parameters["angle_unit"])
    )


def _target_axes(parameters):
    if parameters["axes_target"] == "cartesian":
        return None
    try:
        values = [
            float(word)
            for word in parameters["axes_basis"]
            .replace(";", " ")
            .replace(",", " ")
            .split()
        ]
    except ValueError as exc:
        raise ValueError(
            "Enter nine finite unit-free target-axis components in row order."
        ) from exc
    if len(values) != 9 or not np.all(np.isfinite(values)):
        raise ValueError(
            "Enter nine finite unit-free target-axis components in row order."
        )
    # Native alignment owns orthonormality and handedness admission at apply.
    return np.asarray(values, dtype=np.float64).reshape(3, 3)


def _reference_file_identity(filename):
    """Identify an ordinary local input without reading its coordinate series."""
    try:
        path = Path(filename).expanduser().resolve(strict=True)
        if not path.is_file():
            raise ValueError("The reference path must name a file.")
        details = path.stat()
    except (OSError, ValueError) as exc:
        raise ValueError(
            "Choose an existing local reference file accessible to this Python session."
        ) from exc
    return (
        str(path),
        details.st_dev,
        details.st_ino,
        details.st_size,
        details.st_mtime_ns,
        details.st_ctime_ns,
    )


def _fit_population(system, expression, fallback, structure_index):
    """Resolve declared positional pairs through the native selection boundary."""
    from molsysmt import basic

    text = expression.strip()
    selection = text if text else list(fallback)
    if text.startswith("["):
        import json

        try:
            selection = json.loads(text)
        except ValueError as exc:
            raise ValueError(
                "Use an expression or a JSON list of atom indices."
            ) from exc
        if not isinstance(selection, list) or any(
            isinstance(index, bool) or not isinstance(index, int) for index in selection
        ):
            raise ValueError(
                "Ordered atom indices must be a flat JSON list of integers."
            )
    indices = np.asarray(
        basic.select(
            system,
            selection=selection,
            element="atom",
            structure_indices=[structure_index],
            chemical_state="reference",
        ),
        dtype=np.int64,
    )
    if indices.ndim != 1 or not indices.size:
        raise ValueError("Choose a nonempty fitting atom population.")
    return tuple(int(index) for index in indices)


def _snapshot_reference(references):
    """Retain one selected coordinate slab, with its explicit physical unit."""
    from molsysmt import basic
    from molsysmt import pyunitwizard as puw

    coordinates = basic.get(
        references.file[0],
        element="atom",
        selection=list(references.reference),
        structure_indices=[references.reference_frame],
        coordinates=True,
    )
    if coordinates is None:
        raise ValueError("The reference file must provide molecular coordinates.")
    values, unit = puw.get_value_and_unit(coordinates)
    values = np.array(values, copy=True)
    if values.shape != (1, len(references.reference), 3):
        raise ValueError(
            "Reference coordinates must retain one structure and the selected atom axis."
        )
    if _reference_file_identity(references.file[0]) != references.file:
        raise ValueError("The reference file changed while reading. Review again.")
    values.setflags(write=False)
    return puw.quantity(values, unit)


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
    reference_total: int | None = None
    file: tuple = ()


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
    reference_coordinates: object = None


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
                "reference_kind": "file" if review.references.file else "system",
                "reference_filename": Path(review.references.file[0]).name
                if review.references.file
                else None,
                "reference_n_structures": review.references.reference_total,
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
            allow_repeated=self._parameters["task"] == "fit",
        )
        if self._parameters["task"] == "fit":
            # Coordinate editing applies once per physical structure, in the
            # first requested order; fitting atom-pair order is independent.
            frames = list(dict.fromkeys(frames))
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
        if self._parameters["task"] == "axes":
            _target_axes(self._parameters)
            references = _GeometryReferences(
                fit=population(self._parameters["axes_expression"], atoms)
            )
        elif self._parameters["task"] == "translate":
            _length_vector(self._parameters)
        elif self._parameters["task"] == "rotate":
            _rotation(self._parameters)
            if self._parameters["rotation_center_kind"] == "point":
                _length_vector(self._parameters, "center")
            elif self._parameters["rotation_center_kind"] == "geometric":
                references = _GeometryReferences(center=tuple(int(i) for i in atoms))
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
            if not atoms.size:
                return status, total, frame, atoms, tuple(frames), references
            reference_system = target
            reference_total = total
            file = ()
            if self._parameters["fit_reference_kind"] == "file":
                filename = self._parameters["fit_reference_filename"].strip()
                if not filename:
                    raise ValueError("Choose an external molecular reference file.")
                file = _reference_file_identity(filename)
                reference_system = file[0]
                reference_total = basic.get(reference_system, n_structures=True)
                if reference_total is None or int(reference_total) < 1:
                    raise ValueError(
                        "The reference file must provide molecular structures."
                    )
                reference_total = int(reference_total)
            text = self._parameters["fit_reference_structure"].strip()
            try:
                reference_frame = int(text)
            except ValueError as exc:
                raise ValueError(
                    "Choose an integer reference structure index."
                ) from exc
            if not 0 <= reference_frame < reference_total:
                raise ValueError(
                    "The reference structure index is outside the chosen reference system."
                )
            fit = _fit_population(
                target, self._parameters["fit_expression"], atoms, frame
            )
            reference = _fit_population(
                reference_system,
                self._parameters["fit_reference_expression"],
                fit,
                reference_frame,
            )
            if atoms.size and (len(fit) < 3 or len(reference) != len(fit)):
                raise ValueError(
                    "A rigid fit needs at least three corresponding atom pairs with equal population sizes."
                )
            references = _GeometryReferences(
                fit=fit,
                reference=reference,
                reference_frame=reference_frame,
                reference_total=reference_total,
                file=file,
            )
        return status, total, frame, atoms, tuple(frames), references

    def _prepare_review(self, target):
        status, total, frame, atoms, frames, references = self._resolve(target)
        if not atoms.size:
            return None
        atoms = atoms.copy()
        atoms.setflags(write=False)
        reference_coordinates = (
            _snapshot_reference(references) if references.file else None
        )
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
            reference_coordinates,
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
        if references.file != review.references.file:
            raise ValueError(
                "The reference file changed. Review the coordinate change again."
            )
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
        if review.parameters["task"] == "axes":
            # This native API is flag-free; its ordinary validation always runs.
            parameters.pop("skip_digestion")
            parameters.update(
                principal_axes_of_selection=list(references.fit),
                principal_axes_type=review.parameters["axes_type"],
                weights=None
                if review.parameters["axes_weights"] == "uniform"
                else "masses",
                axes=_target_axes(review.parameters),
                center=review.parameters["axes_center"] == "origin",
                engine="MolSysMT",
            )
        elif review.parameters["task"] == "translate":
            parameters["translation"] = _length_vector(review.parameters)
        elif review.parameters["task"] == "rotate":
            from molsysmt.structure import get_center

            parameters["rotation"] = _rotation(review.parameters)
            kind = review.parameters["rotation_center_kind"]
            # Apply-time only: this check shares the managed edit/read lock.
            parameters["rotation_center"] = (
                get_center(
                    target,
                    selection=atoms.tolist(),
                    structure_indices=list(frames),
                    weights=None,
                    engine="MolSysMT",
                )
                if kind == "geometric"
                else _length_vector(review.parameters, "center")
                if kind == "point"
                else None
            )
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
                    "reference_molecular_system": review.reference_coordinates,
                    "reference_selection_fit": list(range(len(references.reference)))
                    if references.file
                    else list(references.reference),
                    "reference_structure_index": 0
                    if references.file
                    else references.reference_frame,
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
