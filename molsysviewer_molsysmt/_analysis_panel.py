"""Native distance-family queries with bounded pages and explicit source axes."""

from dataclasses import dataclass
from math import isfinite
from secrets import token_urlsafe
from weakref import ref

import numpy as np
from molsysviewer import AddonPanelWidget

from ._analysis_panel_frontend import CSS as ANALYSIS_CSS
from ._analysis_panel_frontend import ESM
from ._panel_frontend import CSS
from ._task_panel import _MolecularTaskPanel, _structures

_DEFAULTS = {
    "task": "distances",
    "relation": "between",
    "pairing": "cartesian",
    "first_endpoint": "atoms",
    "second_endpoint": "atoms",
    "structures": "current",
    "indices": "",
    "pbc": False,
    "neighbor_mode": "cutoff",
    "cutoff": "0.35",
    "cutoff_unit": "nm",
    "count": "5",
}
_METHODS = {
    "distances": "get_distances",
    "minimum": "get_minimum_distances",
    "maximum": "get_maximum_distances",
    "neighbors": "get_neighbors",
}
_PAGE_SIZE = 50


def _parameters(value):
    if not isinstance(value, dict) or set(value) - set(_DEFAULTS):
        raise ValueError("The analysis request contains unsupported fields.")
    result = dict(_DEFAULTS, **value)
    for key, choices in {
        "task": set(_METHODS),
        "relation": {"within", "between"},
        "pairing": {"cartesian", "paired"},
        "first_endpoint": {"atoms", "geometric", "mass"},
        "second_endpoint": {"atoms", "geometric", "mass"},
        "structures": {"current", "all", "indices"},
        "neighbor_mode": {"cutoff", "count"},
        "cutoff_unit": {"nm", "angstrom", "pm"},
    }.items():
        if not isinstance(result[key], str) or result[key] not in choices:
            raise ValueError(
                "Choose supported analysis, population and structure options."
            )
    for key in ("indices", "cutoff", "count"):
        if not isinstance(result[key], str) or len(result[key]) > (
            4096 if key == "indices" else 64
        ):
            raise ValueError("Enter bounded structure and neighborhood parameters.")
    if not isinstance(result["pbc"], bool):
        raise ValueError("Periodic distances must be explicitly enabled or disabled.")
    return result


@dataclass(frozen=True)
class _AnalysisReport:
    token: str
    target: object
    revision: int
    visible_frame: int
    first_draft: dict
    second_draft: dict
    parameters: dict
    frames: list
    first: np.ndarray
    second: np.ndarray
    selections: tuple
    values: object
    native_values: object
    unit: object
    auxiliary: object
    offsets: object
    layout: str
    total: int
    periodic: bool
    software: str


class _AnalysisPanel(_MolecularTaskPanel):
    _esm = ESM
    _css = CSS + ANALYSIS_CSS
    _state_key = "analysis_selection"
    _allow_all = True
    read_only_actions = ("calculate", "refresh", "task", "page", "clear")

    def __init__(self, view=None, **kwargs):
        if not hasattr(AddonPanelWidget, "read_only_actions"):
            raise RuntimeError(
                "Update MolSysViewer to a qualified host with read-only addon panel actions before opening Analysis."
            )
        super().__init__(view=view, **kwargs)
        self._parameters = dict(_DEFAULTS)
        self._second = self._normalize_draft({})
        self._report = None
        self._offset = 0

    def _restore_inputs(self):
        try:
            self._parameters = _parameters(self.state.get("analysis_parameters", {}))
            self._second = self._normalize_draft(
                self.state.get("analysis_selection_2", {})
            )
        except (TypeError, ValueError):
            self._parameters = dict(_DEFAULTS)
            self._second = self._normalize_draft({})
        self._release_task_data()

    def _release_task_data(self):
        if self._report is not None:
            cleanup = getattr(self._report.native_values, "cleanup", None)
            if callable(cleanup):
                # Retain a failing retirement as an error; never report that
                # Clear succeeded while silently abandoning a native resource.
                cleanup()
            self._report = None
        self._offset = 0

    def _diagnostic_inputs(self):
        return (dict(self._draft), dict(self._second), dict(self._parameters))

    def _population(self, target, draft, status):
        if status["state"] != "synchronized" and draft["source"] in {
            "current",
            "saved",
            "region",
        }:
            raise ValueError(
                "Update the scene before using its selection or regions. Choose current molecular data with a category, expression or atom indices instead."
            )
        frame = (
            int(self._view.player.index)
            if draft["context"] == "current"
            else draft["structure_index"]
        )
        if frame >= int(target.structures.n_structures):
            raise ValueError("The selection structure index is outside this system.")
        atoms = self._selection(target, frame, draft=draft, unique=False)
        if not atoms.size:
            raise ValueError("Choose a nonempty atom population for this analysis.")
        return atoms

    def _calculate(self, target):
        import molsysmt as msm

        status = self._owner.get_sync_status()
        if status["state"] not in {"synchronized", "pending", "sync_failed"}:
            raise ValueError(
                "Finish molecular recovery before calculating an analysis."
            )
        p = self._parameters
        first = self._population(target, self._draft, status)
        between = p["relation"] == "between"
        second = self._population(target, self._second, status) if between else first
        frames = _structures(
            p["structures"],
            p["indices"],
            int(target.structures.n_structures),
            int(self._view.player.index),
            allow_repeated=True,
        )
        paired = p["pairing"] == "paired"
        if paired and not between:
            raise ValueError("Corresponding pairs require two explicit populations.")
        centered_a = p["first_endpoint"] != "atoms"
        centered_b = p["second_endpoint"] != "atoms" if between else centered_a
        arguments = {
            "selection": first.tolist(),
            "selection_2": second.tolist() if between else None,
            "structure_indices": frames,
            "pbc": p["pbc"],
            "engine": "MolSysMT",
            "center_of_atoms": centered_a,
            "center_of_atoms_2": centered_b if between else False,
            "weights": "masses" if p["first_endpoint"] == "mass" else None,
            "weights_2": "masses"
            if between and p["second_endpoint"] == "mass"
            else None,
        }
        layout, offsets, auxiliary = "matrix", None, None
        if p["task"] == "neighbors":
            if paired:
                raise ValueError(
                    "Neighbor search uses populations, not corresponding pairs."
                )
            if p["neighbor_mode"] == "cutoff":
                try:
                    cutoff = float(p["cutoff"])
                except ValueError as exc:
                    raise ValueError(
                        "Enter a finite, nonnegative cutoff with its length unit."
                    ) from exc
                if not isfinite(cutoff) or cutoff < 0:
                    raise ValueError(
                        "Enter a finite, nonnegative cutoff with its length unit."
                    )
                arguments["threshold"] = msm.pyunitwizard.quantity(
                    cutoff, p["cutoff_unit"]
                )
                sparse = (
                    cutoff > 0
                    and not (centered_a or centered_b)
                    and len(np.unique(first)) == len(first)
                )
                arguments["output_type"] = "csr" if sparse else "numpy.ndarray"
            else:
                try:
                    count = int(p["count"])
                except ValueError as exc:
                    raise ValueError(
                        "Enter a nonnegative integer neighbor count."
                    ) from exc
                if count < 0:
                    raise ValueError("Enter a nonnegative integer neighbor count.")
                arguments["n_neighbors"] = count
                arguments["output_type"] = "numpy.ndarray"
                sparse = False
            result = self._owner.structure.get_neighbors(**arguments)
            if sparse:
                offsets, auxiliary, values = result
                layout = "csr"
                total = len(auxiliary)
            else:
                auxiliary, values = result
                layout = "neighbors"
                counts = (
                    np.full(
                        auxiliary.shape[0] * auxiliary.shape[1],
                        auxiliary.shape[2],
                        dtype=np.int64,
                    )
                    if auxiliary.ndim == 3
                    else np.fromiter(
                        (len(row) for row in auxiliary.flat), dtype=np.int64
                    )
                )
                offsets = np.r_[0, np.cumsum(counts)]
                total = int(offsets[-1])
        else:
            arguments["pairs"] = paired
            method = getattr(self._owner.structure, _METHODS[p["task"]])
            if p["task"] == "distances":
                # Explicit public native block mode bounds flat matrix work and
                # returns its own disk handle when appropriate. Centers/pairs
                # retain the native eager route; this is no universal RAM bound.
                values = method(**arguments, heavy_mode="force", use_gpu=False)
                total = int(np.prod(values.shape))
                layout = "paired" if paired else "matrix"
            else:
                auxiliary, values = method(**arguments)
                total = len(frames)
                layout = "extrema_paired" if paired else "extrema"
        raw, unit = (
            msm.pyunitwizard.get_value(values),
            msm.pyunitwizard.get_unit(values),
        )
        return _AnalysisReport(
            token_urlsafe(18),
            ref(target),
            status["target_revision"],
            int(self._view.player.index),
            dict(self._draft),
            dict(self._second),
            dict(p),
            frames,
            first,
            second,
            (centered_a, centered_b),
            values,
            raw,
            unit,
            auxiliary,
            offsets,
            layout,
            total,
            bool(p["pbc"] and msm.pbc.has_pbc(target)),
            str(msm.__version__)[:200],
        )

    def _current_report(self, context):
        report = self._report
        if report is None:
            return None
        depends_on_visible = (
            report.parameters["structures"] == "current"
            or report.first_draft["context"] == "current"
            or (
                report.parameters["relation"] == "between"
                and report.second_draft["context"] == "current"
            )
        )
        if (
            self._view.molsys is not report.target()
            or context.get("target_revision") != report.revision
            or context.get("state") not in {"synchronized", "pending", "sync_failed"}
            or (
                depends_on_visible
                and context.get("structure_index") != report.visible_frame
            )
            or (self._draft, self._second, self._parameters)
            != (report.first_draft, report.second_draft, report.parameters)
        ):
            self._release_task_data()
            return None
        for draft, atoms in [
            (report.first_draft, report.first),
            *(
                [(report.second_draft, report.second)]
                if report.parameters["relation"] == "between"
                else []
            ),
        ]:
            if draft["source"] in {"current", "saved", "region"}:
                try:
                    valid = self._owner._read(
                        lambda target, draft=draft, atoms=atoms: np.array_equal(
                            self._population(target, draft, context), atoms
                        ),
                        {},
                    )
                except (ValueError, RuntimeError):
                    valid = False
                if not valid:
                    self._release_task_data()
                    return None
        return report

    def _summary(self):
        r = self._report
        return {
            "id": r.token,
            "method": "molsysmt.structure." + _METHODS[r.parameters["task"]],
            "software": {"molsysmt": r.software},
            "rows": r.total,
            "unit": "nm",
            "first_atoms": len(r.first),
            "second_atoms": len(r.second),
            "structure_indices": r.frames[:200],
            "structures_truncated": len(r.frames) > 200,
            "structure_count": len(r.frames),
            "source_revision": r.revision,
            "periodic": r.periodic,
            "requested_pbc": r.parameters["pbc"],
            "disk_backed": callable(getattr(r.native_values, "cleanup", None)),
        }

    def _page(self, offset):
        import molsysmt as msm

        r = self._report
        if offset and offset >= r.total:
            raise ValueError("That analysis page is outside its result population.")
        rows, samples = [], []
        na = 1 if r.selections[0] else len(r.first)
        nb = 1 if r.selections[1] else len(r.second)
        for position in range(offset, min(r.total, offset + _PAGE_SIZE)):
            if r.layout == "matrix":
                f, a, b = np.unravel_index(position, (len(r.frames), na, nb))
                value = r.native_values[f, a, b]
            elif r.layout == "paired":
                f, a = np.unravel_index(position, (len(r.frames), na))
                b = a
                value = r.native_values[f, a]
            elif r.layout.startswith("extrema"):
                f = position
                if r.layout == "extrema_paired":
                    a = b = int(r.auxiliary[f])
                else:
                    a, b = (int(i) for i in r.auxiliary[f])
                value = r.native_values[f]
            else:
                query = int(np.searchsorted(r.offsets, position, side="right") - 1)
                f, a = divmod(query, na)
                rank = position - int(r.offsets[query])
                if r.layout == "csr":
                    b, value = int(r.auxiliary[position]), r.native_values[position]
                else:
                    b, value = int(r.auxiliary[f, a][rank]), r.native_values[f, a][rank]
            first = "Center A" if r.selections[0] else int(r.first[a])
            second = "Center B" if r.selections[1] else int(r.second[b])
            rows.append([r.frames[f], first, second])
            samples.append(value)
        converted = msm.pyunitwizard.get_value(
            msm.pyunitwizard.quantity(np.asarray(samples, dtype=float), r.unit),
            to_unit="nm",
        )
        for row, value in zip(rows, converted, strict=True):
            row.append(format(float(value), ".9g"))
        return {
            "offset": offset,
            "total": r.total,
            "page_size": _PAGE_SIZE,
            "columns": [
                "Structure index",
                "First endpoint",
                "Second endpoint",
                "Distance (nm)",
            ],
            "rows": rows,
        }

    def _publish(self, *, stage="select", message="", request_id=0):
        if not self._alive or self._view is None or self._view.closed:
            return
        context = self._context()
        context["can_calculate"] = (
            context.get("has_system", False)
            and context.get("n_structures", 0) > 0
            and context["state"] in {"synchronized", "pending", "sync_failed"}
        )
        stage, message = self._retained_diagnostic(context, stage, message)
        report = self._current_report(context)
        self.push_state(
            {
                "request_id": request_id,
                "draft": dict(self._draft),
                "second": dict(self._second),
                "parameters": dict(self._parameters),
                "context": context,
                "stage": stage,
                "message": message,
                "report": self._summary() if report else None,
                "page": self._page(self._offset) if report else None,
            }
        )

    def _perform_action(self, action_id, payload, request_id):
        if set(payload) - {
            "request_id",
            "draft",
            "second",
            "parameters",
            "report_id",
            "offset",
        }:
            raise ValueError("The analysis request contains unsupported fields.")
        draft = self._normalize_draft(payload.get("draft", self._draft))
        second = self._normalize_draft(payload.get("second", self._second))
        parameters = _parameters(payload.get("parameters", self._parameters))
        if (draft, second, parameters) != (self._draft, self._second, self._parameters):
            self._release_task_data()
        self._draft, self._second, self._parameters = draft, second, parameters
        self.set_state(
            {
                self._state_key: dict(draft),
                "analysis_selection_2": dict(second),
                "analysis_parameters": dict(parameters),
            }
        )
        if action_id in {"refresh", "task"}:
            if action_id == "task":
                self._release_task_data()
        elif action_id == "calculate":
            self._release_task_data()
            self._report = self._owner._read(self._calculate, {})
            self._publish(
                stage="report",
                message="Calculation completed. Molecular data and the scene are unchanged.",
                request_id=request_id,
            )
            return
        elif action_id == "clear":
            self._release_task_data()
        elif action_id == "page":
            report = self._current_report(self._context())
            offset = payload.get("offset")
            if report is None or payload.get("report_id") != report.token:
                raise ValueError(
                    "That analysis has expired. Calculate it again for the current inputs."
                )
            if (
                isinstance(offset, bool)
                or not isinstance(offset, int)
                or offset < 0
                or offset % _PAGE_SIZE
            ):
                raise ValueError("Choose an existing analysis page.")
            self._page(offset)
            self._offset = offset
        else:
            raise ValueError("Unsupported Analysis action.")
        self._publish(request_id=request_id)
