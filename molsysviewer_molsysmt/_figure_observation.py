"""Detached native calculation recipes for retained core figures.

The schema is owned by this producer, not a mandatory suite result format.
Input correspondence is declared. Preserved molecular/reference inputs are
still required; the recipe does not authenticate a source or observe raw edits.
"""

import sys
from copy import deepcopy
from importlib import import_module
from inspect import Parameter, signature

import numpy as np


def ordered_indices(values):
    """Encode ordered arithmetic runs, including repetitions and negative steps."""
    values = np.asarray(values, dtype=np.int64)
    if values.ndim != 1:
        raise ValueError("Observation index axes must be one-dimensional.")
    runs, start = [], 0
    while start < len(values):
        end = start + 1
        step = int(values[end]) - int(values[start]) if end < len(values) else 0
        while end < len(values) and int(values[end]) == int(values[start]) + step * (
            end - start
        ):
            end += 1
        runs.append([int(values[start]), step, end - start])
        start = end
    return {
        "encoding": "ordered_arithmetic_runs@1",
        "length": len(values),
        "runs": runs,
    }


def encode(value, *, field="molsysmt.figure.argument"):
    """Preserve binary64 arguments explicitly across Python/JSON/browser copies."""
    import molsysmt as msm

    if value is None or type(value) in {bool, int, str}:
        return value
    if isinstance(value, np.generic):
        return encode(value.item(), field=field)
    if isinstance(value, float):
        return {"encoding": "binary64_hex", "value": value.hex()}
    if msm.pyunitwizard.is_quantity(value):
        return {
            "quantity_record": msm.pyunitwizard.QuantityRecord.from_quantity(
                value, field=field
            ).to_dict(encoding="base64")
        }
    if isinstance(value, np.ndarray):
        if value.ndim == 1 and np.issubdtype(value.dtype, np.integer):
            return ordered_indices(value)
        if np.issubdtype(value.dtype, np.floating):
            return {
                "encoding": "binary64_array_hex@1",
                "dtype": str(value.dtype),
                "shape": list(value.shape),
                "values": [float(item).hex() for item in value.flat],
            }
        return {
            "encoding": "ndarray@1",
            "dtype": str(value.dtype),
            "shape": list(value.shape),
            "values": encode(value.tolist(), field=field),
        }
    if isinstance(value, (list, tuple)):
        if all(type(item) is int for item in value):
            return ordered_indices(value)
        return [
            encode(item, field=field + "." + str(index))
            for index, item in enumerate(value)
        ]
    if isinstance(value, dict) and all(type(key) is str for key in value):
        return {
            key: encode(item, field=field + "." + key) for key, item in value.items()
        }
    raise ValueError(
        "This calculation argument needs an explicit observation encoding."
    )


def capture_call(target, method_path, arguments):
    """Use public native mass readers, then retain exactly the forwarded weights.

    Numeric weights still pass native digestion/validation. There is no local
    weighting formula or normalization. The expert API keeps its native calls.
    """
    import molsysmt as msm

    arguments = dict(arguments)
    masses, mass_records = {}, {}
    for key, selection_key in [("weights", "selection"), ("weights_2", "selection_2")]:
        if isinstance(arguments.get(key), str) and arguments[key] == "masses":
            selected = arguments.get(selection_key)
            if selected is None:
                selected = arguments["selection"]
            value = msm.physchem.get_mass(
                target, element="atom", selection=selected, syntax="MolSysMT"
            )
            arguments[key] = np.asarray(
                msm.pyunitwizard.get_value(value), dtype=np.float64
            ).copy()
            mass_records[key] = encode(
                msm.pyunitwizard.quantity(
                    arguments[key], msm.pyunitwizard.get_unit(value)
                ),
                field="molsysmt.figure.arguments." + key,
            )
            mass_records[key]["forwarded_as"] = "raw_numeric_weights"
            masses[key] = {
                "requested": "masses",
                "method": "molsysmt.physchem.get_mass",
                "unit": str(msm.pyunitwizard.get_unit(value)),
                "definition": signature(msm.physchem.get_mass)
                .parameters["definition"]
                .default,
            }
    module, name = method_path.rsplit(".", 1)
    native = getattr(import_module(module), name)
    defaults = {
        key: parameter.default
        for key, parameter in signature(native).parameters.items()
        if key not in arguments
        and key not in {"molecular_system", "skip_digestion"}
        and parameter.default is not Parameter.empty
    }
    context = {
        "schema": "molsysmt.figure_observation@1",
        "method": method_path,
        "execution_scope": "Public native invocation and forwarded values; automatic device/resource resolution is not a captured execution Context.",
        "software": {
            "molsysmt": str(msm.__version__),
            "numpy": np.__version__,
            "pyunitwizard": str(msm.pyunitwizard.__version__),
        },
        "arguments": encode(
            {key: value for key, value in arguments.items() if key not in mass_records},
            field="molsysmt.figure.arguments",
        )
        | mass_records,
        "native_defaults": encode(defaults, field="molsysmt.figure.native_defaults"),
        "mass_sources": masses,
        "input_shape": {
            "atoms": int(target.get_n_atoms()),
            "structures": int(target.structures.n_structures),
        },
    }
    return arguments, context


def plot_context(report, display_unit, projection):
    """Attach a historical observation, never a current applicability claim."""
    import molsysmt as msm

    if report.calculation_context is None:
        raise ValueError("Recalculate this report to retain its native figure context.")
    context = deepcopy(report.calculation_context)
    if context["arguments"].get("engine") == "MDTraj":
        context["software"]["mdtraj"] = getattr(
            sys.modules.get("mdtraj"), "__version__", None
        )
    native_unit = (
        msm.pyunitwizard.get_unit(report.native_values)
        if msm.pyunitwizard.is_quantity(report.native_values)
        else report.unit
    )
    context.update(
        source={
            "kind": "declared_analysis_input",
            "analysis_id": report.token,
            "managed_revision": report.revision,
            "correspondence": "declared_not_authenticated",
            "raw_edits_observed": False,
        },
        populations={
            "first": ordered_indices(report.first),
            "second": ordered_indices(report.second),
        },
        structure_indices=ordered_indices(report.frames),
        units={"native": str(native_unit), "displayed": str(display_unit)},
        projection=encode(projection),
        reference=None
        if report.reference_frame is None
        else {
            "kind": "same_analysis_input",
            "structure_index": report.reference_frame,
            "atom_indices": ordered_indices(report.second),
        },
        preservation="Preserve the original analysis input, including coordinates, topology, boxes and any reference input. A digest or declared identifier alone is insufficient.",
    )
    return context


def plot_support_limit(view):
    """Keep old core runtimes usable without silently discarding provenance."""
    if "observations" not in signature(view.trajectory_plot.show).parameters:
        return "Retaining calculation details needs a Viewer with figure-observation support. Upgrade the coordinated Viewer/addon pair; the scientific report remains available."
    return ""
