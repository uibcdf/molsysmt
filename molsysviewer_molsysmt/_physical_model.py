"""Bounded display of the public native physical-model inspection.

The raw recipe stays with its native caller. This adapter interprets no force
field, nonbonded criterion, periodic convention or unsupported-control policy.
"""

import json

import numpy as np


def inspect_physical_model(target, frames):
    """Inspect exactly the native construction structure, without a Context."""
    import molsysmt as msm

    reader = getattr(msm.molecular_mechanics, "get_model_recipe", None)
    if not callable(reader):
        raise ValueError("This MolSysMT runtime lacks physical-model inspection.")
    native = reader(target, structure_indices=[frames[0]], engine="OpenMM")
    return native, physical_model_summary(native)


def physical_model_summary(native):
    """Keep a bounded, unit-bearing presentation separate from native science."""
    import molsysmt as msm

    puw = msm.pyunitwizard
    if native.get("schema") != "molsysmt.model_recipe@1":
        raise ValueError("The native physical-model recipe schema is unsupported.")
    rows = []

    def value_text(value):
        unit = ""
        if puw.is_quantity(value):
            # This native contract contains physical-model length quantities;
            # execution settings (temperature, friction, timestep) are separate.
            value, unit = puw.get_value(value, to_unit="nm"), "nm"
        if isinstance(value, np.ndarray):
            if value.size > 100:
                raise ValueError("Inspect this extended recipe through Python.")
            value = value.tolist()
        if isinstance(value, np.generic):
            value = value.item()
        text = (
            "None"
            if value is None
            else json.dumps(value, ensure_ascii=False, allow_nan=False)
            if isinstance(value, (list, tuple, dict))
            else str(value)
        )
        if len(text) > 4096:
            raise ValueError("Inspect this extended recipe through Python.")
        return text, unit

    def add(name, value, origin="native compiled observation"):
        text, unit = value_text(value)
        rows.append([name, text, unit, origin])

    effective = native["effective"]
    for name, entry in native["requested"].items():
        add("Requested: " + name, entry["value"], entry["origin"])
        if "inactive_default" in entry:
            add("Inactive default: " + name, entry["inactive_default"], entry["origin"])
    for key in ("n_particles", "n_constraints", "periodic", "default_box"):
        add("Compiled: " + key, effective[key])
    for position, force in enumerate(effective["nonbonded"]):
        for key, value in force.items():
            add(f"Nonbonded force {position}: {key}", value)
    add("Provider force types", effective["provider_force_types"])
    add("Resource names", native["resources"], "native resource resolution")
    add("Consumed controls", native["consumed_controls"], "native adapter declaration")
    add(
        "Unsupported controls",
        native["unsupported_controls"],
        "native adapter declaration",
    )
    add(
        "Unsupported legacy annotations",
        native["unsupported_legacy_annotations"],
        "native adapter declaration",
    )
    summary = dict(
        schema=native["schema"],
        method="molsysmt.molecular_mechanics.get_model_recipe",
        provenance=native["provenance"],
        construction_structures=np.asarray(
            native["source_structure_indices"], dtype=np.int64
        ).tolist(),
        software=dict(native["software"]),
        periodic=bool(effective["periodic"]),
        rows=rows,
        notice=(
            "Experimental native physical-model inspection. Parameterizes a System when needed, "
            "without a Context, device selection, integrator or molecular preparation. "
            "These are configured properties; some nonbonded controls are inactive for the stated method. "
            "Box vectors are rows in nm. Arbitrary custom-force parameters and construction history "
            "are not reconstructed. This separate inspection is not a snapshot of an execution Context."
        ),
    )
    if len(rows) > 100 or len(json.dumps(summary, allow_nan=False)) > 65536:
        raise ValueError("Inspect this extended recipe through Python.")
    return summary
