"""Explicit scientific-report adoption through existing core color/plot owners."""

from secrets import token_urlsafe

import numpy as np

from ._figure_observation import plot_context, plot_support_limit

_SCALAR_PROPERTIES = {"mass", "reference_charge", "hydrophobicity", "polarity", "sasa"}
_SERIES_LAYOUTS = {
    "matrix",
    "paired",
    "vector_matrix",
    "vector_paired",
    "tuples",
    "property_structures",
    "extrema",
    "extrema_paired",
}


def _color_options(value):
    defaults = {
        "destination": "whole",
        "region": "",
        "palette": "viridis",
        "range": "auto",
        "minimum": "0",
        "maximum": "1",
    }
    if not isinstance(value, dict) or set(value) - set(defaults):
        raise ValueError("Choose supported color destination and scale settings.")
    result = {**defaults, **value}
    for key, choices in {
        "destination": {"whole", "region"},
        "palette": {"viridis", "blue_red"},
        "range": {"auto", "manual"},
    }.items():
        if not isinstance(result[key], str) or result[key] not in choices:
            raise ValueError("Choose supported color destination and scale settings.")
    for key in ("region", "minimum", "maximum"):
        if not isinstance(result[key], str) or len(result[key]) > (
            200 if key == "region" else 64
        ):
            raise ValueError("Enter bounded color destination and range settings.")
    return result


class _VisualReportAdoption:
    @staticmethod
    def _color_limit(report):
        if (
            report.parameters["task"] not in _SCALAR_PROPERTIES
            and report.parameters["task"] != "rmsf"
        ):
            return "Color adoption needs one scalar per source atom or group; no pair, vector, sequence, mode or connectivity aggregation is inferred."
        return ""

    def _result_plot_limit(self, report):
        if report.layout not in _SERIES_LAYOUTS:
            return "This result has no compatible per-structure scalar series."
        if report.frames != list(range(int(self._view.player.n_structures))):
            return "A linked plot needs every loaded structure once, in index order. Choose All structures; missing or repeated observations are not filled or reordered."
        return plot_support_limit(self._view)

    def _adopt_colors(self, report, position, options, request_id):
        from molsysmt import pyunitwizard as puw

        reason = self._color_limit(report)
        if reason:
            raise ValueError(reason)
        options = _color_options(options)
        task = report.parameters["task"]
        observation = None
        if report.layout == "atom_values":
            members = [[int(atom)] for atom in report.first]
            values = puw.get_value(
                puw.quantity(report.native_values, report.unit), to_unit="nm"
            )
            unit = "nm"
        else:
            members, values, unit = (
                report.auxiliary["members"],
                report.values,
                report.unit,
            )
            if report.layout == "property_structures":
                frame, _ = divmod(position, len(members))
                values, observation = values[frame], report.frames[frame]
        values = np.asarray(values, dtype=float)
        if values.shape != (len(members),) or not np.all(np.isfinite(values)):
            raise ValueError(
                "Color adoption requires finite source-mapped scalar values; undefined entries are not filled."
            )
        by_atom = {}
        for population, value in zip(members, values, strict=True):
            for atom in population:
                atom = int(atom)
                if atom in by_atom and by_atom[atom] != float(value):
                    raise ValueError(
                        "Repeated source atoms have conflicting observations; choose an unambiguous scalar report."
                    )
                by_atom[atom] = float(value)
        destination = self._view.whole
        if options["destination"] == "region":
            if options["region"] not in self._view.regions:
                raise ValueError("Choose an existing region as the color destination.")
            destination = self._view.regions[options["region"]]
            scope = destination.atom_indices
            if scope is None:
                raise ValueError(
                    "The color destination needs resolved source atom indices."
                )
            scope = list(scope)
        else:
            scope = list(range(int(self._view.molsys.get_n_atoms())))
        if not scope or any(atom not in by_atom for atom in scope):
            raise ValueError(
                "The report does not cover every atom of this destination. Calculate its full scope or choose a covered region; missing values are not filled."
            )
        target_values = np.asarray([by_atom[atom] for atom in scope])
        physical = unit not in {"", "dimensionless"}
        quantity = puw.quantity(target_values, unit) if physical else target_values
        bounds = None
        if options["range"] == "manual":
            try:
                bounds = [float(options["minimum"]), float(options["maximum"])]
            except ValueError as exc:
                raise ValueError(
                    "Enter finite color bounds in the report's displayed unit."
                ) from exc
            if not np.all(np.isfinite(bounds)) or bounds[0] >= bounds[1]:
                raise ValueError(
                    "Color bounds must be finite, with minimum below maximum."
                )
            if physical:
                bounds = puw.quantity(bounds, unit)
        palette = (
            "viridis"
            if options["palette"] == "viridis"
            else ["#2166ac", "#f7f7f7", "#b2182b"]
        )
        # One existing core setter owns normalization, mutation, persistence and
        # Undo. No new region, incomplete partial layer or private renderer.
        destination.set_color_by_values(
            quantity, element="atom", palette=palette, value_range=bounds, replace=True
        )
        label = "Whole" if options["destination"] == "whole" else options["region"]
        explanation = (
            f" from structure {observation}" if observation is not None else ""
        )
        self._publish(
            stage="scene",
            request_id=request_id,
            message=f"Colored {label} with {task}{explanation} ({unit}). This is a fixed color snapshot; it does not recalculate on structure changes. Clear keeps it; core color controls and Undo own it.",
            scene_action={
                "id": "apply_report_colors",
                "destination": options["destination"],
                "region": options["region"],
                "observation_structure_index": observation,
            },
        )

    def _adopt_result_plot(self, report, position, component, request_id):
        from molsysmt import pyunitwizard as puw

        reason = self._result_plot_limit(report)
        if reason:
            raise ValueError(reason)
        if not isinstance(component, str) or component not in {"x", "y", "z"}:
            raise ValueError("Choose a Cartesian vector component.")
        task = report.parameters["task"]
        projection = {"layout": report.layout}
        if report.layout == "property_structures":
            _, column = divmod(position, len(report.auxiliary["indices"]))
            projection.update(
                element=report.auxiliary["element"],
                index=int(report.auxiliary["indices"][column]),
            )
            values = np.asarray(report.values)[:, column]
            unit = report.unit
            label = f"SASA · {report.auxiliary['element']} {report.auxiliary['indices'][column]}"
        elif report.layout.startswith("extrema"):
            values = np.asarray(
                puw.get_value(
                    puw.quantity(report.native_values, report.unit), to_unit="nm"
                )
            )
            unit, label = "nm", task.title() + " distance in each structure"
            projection["native_endpoint_output"] = report.auxiliary
        else:
            _, a, b, _ = self._row(position)
            projection.update(first_position=int(a), second_position=int(b))
            native = (
                report.native_values[:, a]
                if report.layout in {"paired", "vector_paired", "tuples"}
                else report.native_values[:, a, b]
            )
            unit = (
                report.parameters["angle_unit"] if report.layout == "tuples" else "nm"
            )
            values = np.asarray(
                puw.get_value(puw.quantity(native, report.unit), to_unit=unit)
            )
            if report.layout == "tuples":
                label = (
                    task.title()
                    + " · atoms "
                    + ", ".join(map(str, report.auxiliary[a]))
                )
            else:
                first = (
                    "center A" if report.selections[0] else f"atom {report.first[a]}"
                )
                second = (
                    "center B" if report.selections[1] else f"atom {report.second[b]}"
                )
                label = f"{task.title()} · {first} → {second}"
            if report.layout.startswith("vector"):
                projection["component"] = component
                values = values[:, {"x": 0, "y": 1, "z": 2}[component]]
                label += " · " + component.upper()
        if values.shape != (len(report.frames),) or not np.all(np.isfinite(values)):
            raise ValueError(
                "A linked plot requires a finite scalar in every loaded structure; undefined values are not filled."
            )
        tag = "molsysmt-report-" + token_urlsafe(12)
        self._view.trajectory_plot.show(
            {label: values},
            tag=tag,
            title=label,
            x_label="Structure index",
            y_label=f"Value ({unit})",
            observations=[plot_context(report, unit, projection)],
        )
        self._publish(
            stage="scene",
            request_id=request_id,
            message="Added the selected observation's structure series to core Plots. Clicking a point navigates its source structure; Clear keeps the plot.",
            scene_action={"id": "add_result_plot", "plot_tag": tag},
        )
