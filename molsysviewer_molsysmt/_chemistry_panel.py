"""Bounded inspection of native stored-chemistry and hydrogen reports."""

from collections import Counter
from dataclasses import dataclass
from secrets import token_urlsafe
from weakref import ref

import numpy as np
from molsysviewer import AddonPanelWidget
from molsysviewer.system_edits import SystemEditPendingError

from ._chemistry_panel_frontend import CSS as CHEMISTRY_CSS
from ._chemistry_panel_frontend import ESM
from ._panel_frontend import CSS
from ._task_panel import _MolecularTaskPanel

_PARAMETERS = {"task": "chemistry", "state_mode": "reference", "state_index": "0"}
_METHODS = {
    "chemistry": "get_chemical_readiness",
    "hydrogens": "get_hydrogen_inventory",
}
_PAGE_SIZE = 50
_TEXT_LIMIT = 200
_BOND_FIELDS = {
    "bond_id",
    "bond_type",
    "bond_order",
    "bond_is_aromatic",
    "bond_stereochemistry",
    "covalent_multiplicity",
}


def _parameters(value):
    if not isinstance(value, dict) or set(value) - set(_PARAMETERS):
        raise ValueError("The chemistry request contains unsupported fields.")
    result = dict(_PARAMETERS, **value)
    if result["task"] not in _METHODS or result["state_mode"] not in {
        "reference",
        "structure",
        "index",
    }:
        raise ValueError("Choose a supported report and chemical state.")
    text = result["state_index"]
    if not isinstance(text, str) or len(text) > 64:
        raise ValueError("Enter a nonnegative chemical state index.")
    if result["state_mode"] == "index":
        try:
            index = int(text)
        except ValueError as exc:
            raise ValueError("Enter a nonnegative chemical state index.") from exc
        if index < 0:
            raise ValueError("Enter a nonnegative chemical state index.")
    return result


def _text(value):
    if isinstance(value, np.generic):
        value = value.item()
    text = "Unknown" if value is None else str(value)
    return text[:_TEXT_LIMIT] + ("…" if len(text) > _TEXT_LIMIT else "")


def _field_summary(name, field):
    return {
        "name": name,
        "axis": "bond" if name in _BOND_FIELDS else "atom",
        "status": _text(field["status"]),
        "total": len(field["indices"]),
        **{
            key: len(field[key + "_indices"])
            for key in ("present", "missing", "unsupported", "conflict")
        },
        "unit": _text(field["unit"]) if "unit" in field else "",
    }


@dataclass(frozen=True)
class _ChemistryReport:
    token: str
    target: object
    revision: int
    visible_frame: int
    draft: dict
    parameters: dict
    data: dict


class _ChemistryPanel(_MolecularTaskPanel):
    _esm = ESM
    _css = CSS + CHEMISTRY_CSS
    _state_key = "chemistry_selection"
    _allow_all = True
    read_only_actions = ("inspect", "refresh", "task", "page", "clear")

    def __init__(self, view=None, **kwargs):
        if not hasattr(AddonPanelWidget, "read_only_actions"):
            raise RuntimeError(
                "Update MolSysViewer to a qualified host with read-only addon panel actions before opening Chemistry."
            )
        super().__init__(view=view, **kwargs)
        self._parameters = dict(_PARAMETERS)
        self._report = None
        self._detail = ""
        self._offset = 0

    def _restore_inputs(self):
        try:
            self._parameters = _parameters(self.state.get("chemistry_parameters", {}))
        except (TypeError, ValueError):
            self._parameters = dict(_PARAMETERS)
        self._release_task_data()

    def _release_task_data(self):
        self._report = None
        self._detail = ""
        self._offset = 0

    def _diagnostic_inputs(self):
        return (dict(self._draft), dict(self._parameters))

    def _calculate(self, target):
        status = self._owner.get_sync_status()
        if status["state"] not in {"synchronized", "pending", "sync_failed"}:
            raise ValueError("Finish molecular recovery before inspecting chemistry.")
        if status["state"] != "synchronized" and self._draft["source"] in {
            "current",
            "saved",
            "region",
        }:
            raise ValueError(
                "Update the scene before using its selection or regions. "
                "You can inspect the current molecular data with Whole system, "
                "a category, an expression or explicit atom indices."
            )
        count = int(target.structures.n_structures)
        visible_frame = int(self._view.player.index)
        frame = (
            visible_frame
            if self._draft["context"] == "current"
            else self._draft["structure_index"]
        )
        if not count and self._draft["context"] == "current":
            frame = None
        elif frame >= count:
            raise ValueError("The inspection structure index is outside this system.")
        atoms = self._selection(target, frame)
        state = (
            int(self._parameters["state_index"])
            if self._parameters["state_mode"] == "index"
            else self._parameters["state_mode"]
        )
        method = getattr(self._owner.physchem, _METHODS[self._parameters["task"]])
        data = method(
            selection=atoms,
            structure_indices="all" if frame is None else [frame],
            chemical_state=state,
        )
        return _ChemistryReport(
            token_urlsafe(18),
            ref(target),
            status["target_revision"],
            visible_frame,
            dict(self._draft),
            dict(self._parameters),
            data,
        )

    def _current_report(self, context):
        report = self._report
        if report is not None and (
            self._view.molsys is not report.target()
            or context.get("target_revision") != report.revision
            or context.get("structure_index") != report.visible_frame
            or context.get("state") not in {"synchronized", "pending", "sync_failed"}
            or report.draft != self._draft
            or report.parameters != self._parameters
        ):
            self._release_task_data()
        if self._report is not None and self._draft["source"] in {
            "current",
            "saved",
            "region",
        }:
            try:
                current = self._owner._read(
                    lambda target: self._selection(
                        target, self._report.data["structure_index"]
                    ),
                    {},
                )
                valid = np.array_equal(current, self._report.data["atom_indices"])
            except (ValueError, SystemEditPendingError):
                valid = False
            if not valid:
                self._release_task_data()
        return self._report

    def _summary(self):
        report, data = self._report, self._report.data
        result = {
            "id": report.token,
            "schema": _text(data["schema"]),
            "method": _text(data["method"]),
            "software": {k: _text(v) for k, v in data["software"].items()},
            "n_atoms": len(data["atom_indices"]),
            "structure_index": data["structure_index"],
            "chemical_state_index": data["chemical_state_index"],
            "explicit_hydrogens": len(data["explicit_hydrogen_atom_indices"]),
            "unassessed_checks": [_text(x) for x in data["unassessed_checks"]],
            "source_revision": report.revision,
        }
        if report.parameters["task"] == "chemistry":
            connectivity = data["connectivity"]
            result.update(
                chemical_state_status=_text(data["chemical_state_status"]),
                fields=[_field_summary(k, v) for k, v in data["fields"].items()],
                connectivity={
                    "declared_completeness": _text(
                        connectivity["declared_completeness"]
                    ),
                    "examined_bonds": len(connectivity["examined_bond_indices"]),
                    "invalid_bonds": len(connectivity["invalid_bond_indices"]),
                    "incident_bonds": len(data["bond_indices"]),
                    "crossing_bonds": len(connectivity["crossing_bond_indices"]),
                },
            )
            datasets = [(k, k.replace("_", " ")) for k in data["fields"]]
            datasets += [
                ("incident_bonds", "Selected-incident bonds"),
                ("invalid_bonds", "Invalid bonds in examined state"),
                ("explicit_hydrogens", "Selected explicit H atoms"),
            ]
        else:
            result.update(
                status=_text(data["status"]),
                count_convention=_text(data["count_convention"]),
                issue_counts=[
                    {"reason": _text(k), "count": v}
                    for k, v in Counter(
                        x["reason_code"] for x in data["issues"]
                    ).items()
                ],
            )
            datasets = [
                ("counts", "Per-atom hydrogen counts"),
                ("parent_pairs", "Parent–H pairs"),
                ("issues", "Native inventory issues"),
                ("explicit_hydrogens", "Selected explicit H atoms"),
            ]
        result["datasets"] = [{"id": k, "label": label} for k, label in datasets]
        return result

    def _page(self, summary, *, dataset=None, offset=None):
        data = self._report.data
        choices = {row["id"] for row in summary["datasets"]}
        key = dataset or self._detail or summary["datasets"][0]["id"]
        start = self._offset if offset is None else offset
        if key not in choices:
            raise ValueError("Choose an existing report table.")
        if key in data.get("fields", {}):
            field = data["fields"][key]
            total = len(field["indices"])
            columns = [
                "Bond index" if key in _BOND_FIELDS else "Atom index",
                "Finite position" if key == "coordinates" else "Value",
                "Coverage",
                "Declared origin",
            ]

            def contains(name, index):
                # Native report index populations are sorted source indices.
                # Inspect only the requested page, without copying full sets.
                indices = field[name + "_indices"]
                position = np.searchsorted(indices, index)
                return position < len(indices) and indices[position] == index

            def row(i):
                index = int(field["indices"][i])
                labels = [
                    name
                    for name in ("present", "missing", "unsupported", "conflict")
                    if contains(name, index)
                ]
                return [
                    index,
                    field["values"][i],
                    ", ".join(labels),
                    field["origin"][i],
                ]
        elif key == "counts":
            total = len(data["atom_indices"])
            columns = [
                "Atom index",
                "Indexed H neighbors",
                "Stored non-indexed H",
                "Total H",
            ]

            def row(i):
                values = [
                    data[k][i]
                    for k in (
                        "indexed_hydrogen_counts",
                        "missing_hydrogen_counts",
                        "total_hydrogen_counts",
                    )
                ]
                return [
                    int(data["atom_indices"][i]),
                    *(None if int(v) == -1 else int(v) for v in values),
                ]
        elif key == "issues":
            total, columns = len(data["issues"]), ["Atom index", "Reason", "Diagnostic"]

            def row(i):
                item = data["issues"][i]
                return [
                    item["atom_index"],
                    item["reason_code"],
                    item["diagnostic_code"],
                ]
        elif key == "parent_pairs":
            total, columns = (
                len(data["parent_hydrogen_pairs"]),
                ["Parent atom index", "H atom index"],
            )

            def row(i):
                return data["parent_hydrogen_pairs"][i]
        elif key == "incident_bonds":
            total, columns = (
                len(data["bond_indices"]),
                ["Bond index", "Atom 1", "Atom 2", "Declared evidence"],
            )

            def row(i):
                return [
                    data["bond_indices"][i],
                    *data["bonded_atom_pairs"][i],
                    data["connectivity"]["evidence"][i],
                ]
        else:
            values = (
                data["connectivity"]["invalid_bond_indices"]
                if key == "invalid_bonds"
                else data["explicit_hydrogen_atom_indices"]
            )
            total, columns = (
                len(values),
                ["Bond index" if key == "invalid_bonds" else "Atom index"],
            )

            def row(i):
                return [values[i]]

        if start and start >= total:
            raise ValueError("That report page is outside its source population.")
        values = [row(i) for i in range(start, min(total, start + _PAGE_SIZE))]
        return {
            "dataset": key,
            "offset": start,
            "total": total,
            "page_size": _PAGE_SIZE,
            "columns": columns,
            "rows": [[_text(v) for v in item] for item in values],
            "unit": data.get("fields", {}).get(key, {}).get("unit", ""),
        }

    def _publish(self, *, stage="select", message="", request_id=0):
        if not self._alive or self._view is None or self._view.closed:
            return
        context = self._context()
        context["can_inspect"] = context.get("has_system", False) and context[
            "state"
        ] in {"synchronized", "pending", "sync_failed"}
        stage, message = self._retained_diagnostic(context, stage, message)
        report = self._current_report(context)
        summary = self._summary() if report else None
        self.push_state(
            {
                "request_id": request_id,
                "draft": dict(self._draft),
                "parameters": dict(self._parameters),
                "context": context,
                "stage": stage,
                "message": message,
                "report": summary,
                "page": self._page(summary) if report else None,
            }
        )

    def _perform_action(self, action_id, payload, request_id):
        if set(payload) - {
            "request_id",
            "draft",
            "parameters",
            "report_id",
            "dataset",
            "offset",
        }:
            raise ValueError("The chemistry request contains unsupported fields.")
        draft = self._normalize_draft(payload.get("draft", self._draft))
        parameters = _parameters(payload.get("parameters", self._parameters))
        if draft != self._draft or parameters != self._parameters:
            self._release_task_data()
        self._draft, self._parameters = draft, parameters
        self.set_state(
            {self._state_key: dict(draft), "chemistry_parameters": dict(parameters)}
        )
        if action_id in {"refresh", "task"}:
            if action_id == "task":
                self._release_task_data()
        elif action_id == "inspect":
            self._release_task_data()
            self._report = self._owner._read(self._calculate, {})
            self._publish(
                stage="report",
                message="Inspection completed. Molecular data are unchanged.",
                request_id=request_id,
            )
            return
        elif action_id == "page":
            report = self._current_report(self._context())
            if report is None or payload.get("report_id") != report.token:
                raise ValueError(
                    "That report has expired. Inspect the current system again."
                )
            key, offset = payload.get("dataset"), payload.get("offset")
            choices = {row["id"] for row in self._summary()["datasets"]}
            if (
                key not in choices
                or isinstance(offset, bool)
                or not isinstance(offset, int)
                or offset < 0
                or offset % _PAGE_SIZE
            ):
                raise ValueError("Choose an existing report table and page.")
            self._page(self._summary(), dataset=key, offset=offset)
            self._detail, self._offset = key, offset
        elif action_id == "clear":
            self._release_task_data()
        else:
            raise ValueError("Unsupported Chemistry action.")
        self._publish(request_id=request_id)
