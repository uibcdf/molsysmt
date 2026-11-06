"""Native molecular analyses with bounded pages and explicit source axes."""

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
    "reference_structure": "0",
    "reference_population": "same",
    "weighting": "uniform",
}
_CONFORMATION_METHODS = {
    "rmsd": "get_rmsd",
    "least_rmsd": "get_least_rmsd",
    "gyration": "get_radius_of_gyration",
    "rmsf": "get_rmsf",
}
_METHODS = {
    "distances": "get_distances",
    "minimum": "get_minimum_distances",
    "maximum": "get_maximum_distances",
    "neighbors": "get_neighbors",
    **_CONFORMATION_METHODS,
}
_PAGE_SIZE = 50
_SCENE_ACTIONS = {
    "select_participants",
    "focus_participants",
    "add_live_distance",
    "add_structure_plot",
}


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
        "reference_population": {"same", "second"},
        "weighting": {"uniform", "masses"},
    }.items():
        if not isinstance(result[key], str) or result[key] not in choices:
            raise ValueError(
                "Choose supported analysis, population and structure options."
            )
    for key in ("indices", "cutoff", "count", "reference_structure"):
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
    reference_frame: int | None = None


def _uses_second(parameters):
    if parameters["task"] in _CONFORMATION_METHODS:
        return (
            parameters["task"] in {"rmsd", "least_rmsd"}
            and parameters["reference_population"] == "second"
        )
    return parameters["relation"] == "between"


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
        if p["task"] in _CONFORMATION_METHODS:
            return self._calculate_conformation(target, status, first)
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

    def _calculate_conformation(self, target, status, atoms):
        import molsysmt as msm

        p = self._parameters
        frames = _structures(
            p["structures"],
            p["indices"],
            int(target.structures.n_structures),
            int(self._view.player.index),
            allow_repeated=True,
        )
        arguments = {
            "selection": atoms.tolist(),
            "structure_indices": frames,
            "engine": "MolSysMT",
        }
        reference_frame = None
        reference_atoms = np.empty(0, dtype=np.int64)
        if p["task"] in {"rmsd", "least_rmsd"}:
            try:
                reference_frame = int(p["reference_structure"])
            except ValueError as exc:
                raise ValueError(
                    "Choose an integer reference structure index."
                ) from exc
            if not 0 <= reference_frame < int(target.structures.n_structures):
                raise ValueError(
                    "The reference structure index is outside this system."
                )
            reference_atoms = (
                self._population(target, self._second, status)
                if _uses_second(p)
                else atoms
            )
            if len(reference_atoms) != len(atoms):
                raise ValueError(
                    "Query and reference populations need equal atom counts in the intended correspondence order."
                )
            arguments.update(
                reference_selection=reference_atoms.tolist(),
                reference_structure_index=reference_frame,
                use_gpu=False,
            )
        elif p["task"] == "gyration":
            arguments.update(
                weights="masses" if p["weighting"] == "masses" else None, use_gpu=False
            )
        result = getattr(self._owner.structure, _CONFORMATION_METHODS[p["task"]])(
            **arguments
        )
        raw = np.asarray(msm.pyunitwizard.get_value(result))
        count = len(atoms) if p["task"] == "rmsf" else len(frames)
        if raw.shape != (count,) or not np.all(np.isfinite(raw)):
            raise ValueError(
                "The native result does not provide finite values on the declared atom or structure axis."
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
            atoms,
            reference_atoms,
            (False, False),
            result,
            raw,
            msm.pyunitwizard.get_unit(result),
            None,
            None,
            "atom_values" if p["task"] == "rmsf" else "structure_values",
            count,
            False,
            str(msm.__version__)[:200],
            reference_frame,
        )

    def _current_report(self, context):
        report = self._report
        if report is None:
            return None
        depends_on_visible = (
            report.parameters["structures"] == "current"
            or report.first_draft["context"] == "current"
            or (
                _uses_second(report.parameters)
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
                if _uses_second(report.parameters)
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
        conformation = r.parameters["task"] in _CONFORMATION_METHODS
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
            "requested_pbc": r.parameters["pbc"] if not conformation else False,
            "disk_backed": callable(getattr(r.native_values, "cleanup", None)),
            "live_distance_unavailable": self._live_distance_limit(r),
            "family": "conformation" if conformation else "distance",
            "result_axis": "atom"
            if r.layout == "atom_values"
            else "structure"
            if conformation
            else "pair",
            "reference_structure_index": r.reference_frame,
            "plot_unavailable": self._plot_limit(r),
        }

    def _plot_limit(self, report):
        if report.layout != "structure_values":
            return "This result is not indexed by one scalar per structure."
        if report.frames != list(range(int(self._view.player.n_structures))):
            return "A trajectory plot needs every loaded structure once, in index order. Choose All structures to calculate that scope."
        return ""

    def _row(self, position):
        """Resolve native row axes once for tables and deliberate scene actions."""
        r = self._report
        na = 1 if r.selections[0] else len(r.first)
        nb = 1 if r.selections[1] else len(r.second)
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
        return int(f), int(a), int(b), value

    @staticmethod
    def _live_distance_limit(report):
        if report.parameters["task"] in _CONFORMATION_METHODS:
            return "This result is not a pair distance."
        if report.periodic:
            return "A live distance uses nonperiodic coordinates; this result uses a periodic image."
        if "mass" in (
            report.parameters["first_endpoint"],
            report.parameters["second_endpoint"]
            if report.parameters["relation"] == "between"
            else report.parameters["first_endpoint"],
        ):
            return "A live distance uses geometric centers, not mass-weighted centers."
        return ""

    def _page(self, offset):
        import molsysmt as msm

        r = self._report
        if offset and offset >= r.total:
            raise ValueError("That analysis page is outside its result population.")
        if r.layout in {"atom_values", "structure_values"}:
            stop = min(r.total, offset + _PAGE_SIZE)
            values = msm.pyunitwizard.get_value(
                msm.pyunitwizard.quantity(r.native_values[offset:stop], r.unit),
                to_unit="nm",
            )
            axis = r.first if r.layout == "atom_values" else r.frames
            return {
                "offset": offset,
                "total": r.total,
                "page_size": _PAGE_SIZE,
                "columns": [
                    "Atom index" if r.layout == "atom_values" else "Structure index",
                    "Value (nm)",
                ],
                "rows": [
                    [int(axis[i]), format(float(value), ".9g")]
                    for i, value in zip(range(offset, stop), values, strict=True)
                ],
            }
        rows, samples = [], []
        for position in range(offset, min(r.total, offset + _PAGE_SIZE)):
            f, a, b, value = self._row(position)
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

    def _scene_action(self, action_id, payload, request_id):
        # The host transport holds its managed-edit lock around this handler.
        # Reader callbacks only validate; core scene calls happen after return.
        context = self._context()
        if context.get("state") != "synchronized":
            raise ValueError("Update the scene before using an analysis result in it.")
        report = self._current_report(context)
        if report is None or payload.get("report_id") != report.token:
            raise ValueError(
                "That analysis has expired. Calculate it again for the current inputs."
            )
        if action_id == "add_structure_plot":
            reason = self._plot_limit(report)
            if reason:
                raise ValueError(reason)
            import molsysmt as msm

            if not self._owner._read(lambda target: target is report.target(), {}):
                raise ValueError(
                    "The calculated structure series no longer belongs to this system."
                )
            values = msm.pyunitwizard.get_value(report.values, to_unit="nm")
            titles = {
                "rmsd": "RMSD without superposition",
                "least_rmsd": "RMSD after optimal superposition",
                "gyration": "Radius of gyration",
            }
            tag = "molsysmt-" + report.parameters["task"] + "-" + report.token
            self._view.trajectory_plot.show(
                {titles[report.parameters["task"]]: values},
                tag=tag,
                title=titles[report.parameters["task"]],
                x_label="Structure index",
                y_label="Length (nm)",
            )
            self._publish(
                stage="scene",
                request_id=request_id,
                message="Added a trajectory plot. It belongs to core Plots and remains after clearing this report. Move or close Studio if it covers the plot.",
                scene_action={"id": action_id, "plot_tag": tag},
            )
            return
        position = payload.get("row_index")
        if (
            isinstance(position, bool)
            or not isinstance(position, int)
            or not self._offset
            <= position
            < min(report.total, self._offset + _PAGE_SIZE)
        ):
            raise ValueError("Choose a result row on the current page.")
        if report.layout == "atom_values":
            first, second, observation_structure = (
                [int(report.first[position])],
                [],
                None,
            )
        elif report.layout == "structure_values":
            first, second = report.first.tolist(), report.second.tolist()
            observation_structure = report.frames[position]
        else:
            f, a, b, _ = self._row(position)
            first = (
                report.first.tolist()
                if report.selections[0]
                else [int(report.first[a])]
            )
            second = (
                report.second.tolist()
                if report.selections[1]
                else [int(report.second[b])]
            )
            observation_structure = report.frames[f]
        participants = list(dict.fromkeys(first + second))

        def validate(target):
            if target is not report.target() or any(
                atom < 0 or atom >= int(target.topology.n_atoms)
                for atom in participants
            ):
                raise ValueError(
                    "The result participants no longer belong to this system."
                )

        self._owner._read(validate, {})
        current = int(self._view.player.index)
        outcome = {
            "id": action_id,
            "row_index": position,
            "structure_index": current,
            "observation_structure_index": observation_structure,
        }
        if action_id == "select_participants":
            self._view.active_selection.set(participants)
            message = f"Selected {len(participants)} participant atoms. Molecular data are unchanged."
            if self._current_report(self._context()) is None:
                message += " The result context changed; calculate it again before using another row."
        elif action_id == "focus_participants":
            self._view.focus_selection(participants, structure_indices=[current])
            message = f"Focused participant atoms in visible structure {current}."
        else:
            reason = self._live_distance_limit(report)
            if reason:
                raise ValueError(reason)
            measurement = self._view.measurements.add_distance(
                first, second, endpoint_policy="centroid"
            )
            outcome["measurement_tag"] = measurement.tag
            message = (
                f"Added live distance {measurement.tag} in Measures. It follows the visible "
                f"structure; the selected result row remains in structure {observation_structure}."
            )
        self._publish(
            stage="scene", message=message, request_id=request_id, scene_action=outcome
        )

    def _publish(self, *, stage="select", message="", request_id=0, scene_action=None):
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
                "scene_action": scene_action,
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
            "row_index",
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
        if action_id in _SCENE_ACTIONS:
            self._scene_action(action_id, payload, request_id)
            return
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
