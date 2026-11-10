"""Shared private model-request review for explicit native tools.

This is not an engine-neutral effective recipe or a competing mechanics store.
Native construction still owns implementation and unsupported controls (#582).
"""

import numpy as np


def _mechanical_model(target, *, purpose="calculation"):
    """Review stored requests and native defaults without constructing an engine."""
    import molsysmt as msm
    from molsysmt import pyunitwizard as puw
    from molsysmt.configure import default_attribute

    # Native #582 owns these independently stored controls. The GUI must not
    # imply that displaying an ignored input makes it an effective setting.
    unsupported = [
        name
        for name in (
            "solute_dielectric",
            "solvent_dielectric",
            "kappa",
            "salt_concentration",
            "cutoff_distance",
        )
        if msm.basic.has_attribute(target, name)
    ]
    if unsupported:
        raise ValueError(
            f"This native {purpose} adapter cannot independently apply stored "
            + ", ".join(unsupported)
            + f". Resolve the model explicitly before {purpose} (MolSysMT #582)."
        )
    units = {
        "switch_distance": "nm",
        "temperature": "K",
        "friction": "1/ps",
        "time_step": "ps",
    }
    fields = (
        "forcefield",
        "water_model",
        "implicit_solvent",
        "constraints",
        "non_bonded_method",
        "switch_distance",
        "dispersion_correction",
        "ewald_error_tolerance",
        "integrator",
        "temperature",
        "friction",
        "time_step",
    )
    result = []
    for name in fields:
        stored = msm.basic.has_attribute(target, name)
        value = (
            msm.basic.get(target, **{name: True}) if stored else default_attribute[name]
        )
        unit = units.get(name, "")
        if unit and value is not None:
            if not puw.is_quantity(value):
                value = puw.quantity(value)
            value = float(puw.get_value(value, to_unit=unit))
            if not np.isfinite(value):
                raise ValueError("Mechanical model parameters must be finite.")
        elif isinstance(value, (list, tuple)):
            if (
                any(not isinstance(item, str) or len(item) > 200 for item in value)
                or len(value) > 100
            ):
                raise ValueError(
                    "Use the Python API for this extended model definition."
                )
            value = tuple(value)
        elif isinstance(value, np.generic):
            value = value.item()
        elif not isinstance(value, (str, bool, float, int, type(None))):
            raise ValueError("Use the Python API for this model definition.")
        if isinstance(value, str) and len(value) > 200:
            raise ValueError("Use the Python API for this extended model definition.")
        result.append((name, value, unit, "stored" if stored else "native_default"))
    return tuple(result)
