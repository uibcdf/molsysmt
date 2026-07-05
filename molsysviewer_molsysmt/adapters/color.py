"""Color adapter — MolSysMT scalar properties prepared for MolSysViewer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..access import has_system


@dataclass(frozen=True)
class ColorValues:
    property: str
    element: str
    values: list[float]
    unit: str | None = None


_SUPPORTED_PROPERTIES: dict[str, tuple[str, str | None]] = {
    "charge": ("group", "elementary_charge"),
    "mass": ("group", "dalton"),
    "atomic_radius": ("atom", "nanometer"),
}


def supported_properties() -> tuple[str, ...]:
    """Return the robust first-pass property names supported by the addon."""
    return tuple(_SUPPORTED_PROPERTIES)


def property_values(view: Any, property: str) -> ColorValues:
    """Return scalar values for a supported MolSysMT property.

    The adapter operates on the view-as-form and returns plain floats, with the
    target MolSysViewer element level attached for cardinality validation by the
    caller.
    """
    if not has_system(view):
        raise ValueError("No molecular system attached.")
    if property not in _SUPPORTED_PROPERTIES:
        raise ValueError(f"Unsupported color property: {property!r}")

    import numpy as np
    import molsysmt as msm
    from molsysmt import pyunitwizard as puw

    element, unit = _SUPPORTED_PROPERTIES[property]
    if property == "charge":
        raw = msm.physchem.get_charge(view, element=element)
    elif property == "mass":
        raw = msm.physchem.get_mass(view, element=element)
    elif property == "atomic_radius":
        raw = msm.physchem.get_atomic_radius(view, element=element)
    else:  # pragma: no cover - guarded above
        raise ValueError(f"Unsupported color property: {property!r}")

    try:
        values = puw.get_value(raw, to_unit=unit) if unit is not None else puw.get_value(raw)
    except Exception:
        values = raw
    values = np.asarray(values, dtype=float).reshape(-1).tolist()

    expected = _expected_count(view, element)
    if len(values) != expected:
        raise ValueError(
            f"Color property {property!r} produced {len(values)} value(s), "
            f"but element {element!r} requires {expected}."
        )
    return ColorValues(property=property, element=element, values=values, unit=unit)


def _expected_count(view: Any, element: str) -> int:
    import molsysmt as msm

    if element == "atom":
        return int(msm.get(view, n_atoms=True))
    if element == "group":
        return int(msm.get(view, element="group", n_groups=True))
    raise ValueError(f"Unsupported color element: {element!r}")
