"""Resolving explicit units in legacy H5MSM structural datasets."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import FormatError

_FIELDS = {
    "coordinates": ("length_unit", "nm"),
    "box": ("length_unit", "nm"),
    "time": ("time_unit", "ps"),
    "velocities": ("velocity_unit", "nm/ps"),
    "b_factor": ("b_factor_unit", "nm**2"),
    "temperature": ("temperature_unit", "K"),
    "potential_energy": ("energy_unit", "kJ/mol"),
    "kinetic_energy": ("energy_unit", "kJ/mol"),
}


def _declarations(dataset, attribute, *, include_dataset=True):
    """Read dataset, structural-group, and root declarations without defaults."""
    declarations = []
    locations = [(dataset.parent, attribute), (dataset.file, attribute)]
    if include_dataset:
        locations.insert(0, (dataset, "unit"))
    for owner, key in locations:
        if key in owner.attrs:
            unit = owner.attrs[key]
            if isinstance(unit, bytes):
                unit = unit.decode()
            declarations.append((f"{owner.name}@{key}", unit))
    return declarations


def legacy_dataset_unit(dataset):
    """Resolve one explicit unit, rejecting missing or inconsistent metadata.

    Equivalent spellings are accepted, but different scales or offsets are not.
    Legacy group/root declarations remain supported. Velocity units may be
    derived from explicit length/time declarations, never session defaults.
    B factors require their own unit because legacy writers negotiated them
    independently of coordinate units.
    """
    field = dataset.name.rsplit("/", 1)[-1]
    attribute, expected = _FIELDS[field]
    declarations = _declarations(dataset, attribute)
    if field == "velocities":
        lengths = _declarations(dataset, "length_unit", include_dataset=False)
        times = _declarations(dataset, "time_unit", include_dataset=False)
        for length_source, length in lengths:
            for time_source, time in times:
                declarations.append(
                    (f"{length_source}/{time_source}", f"{length}/{time}")
                )
    if not declarations:
        raise FormatError(
            reason=f"H5MSM dataset {dataset.name!r} has no explicit unit declaration.",
            caller="molsysmt.h5msm",
        )
    reference = None
    for source, unit in declarations:
        try:
            converted = puw.get_value(
                puw.quantity([0.0, 1.0], puw.unit(unit)), to_unit=expected
            )
        except Exception as error:
            raise FormatError(
                reason=(
                    f"Invalid unit {unit!r} at {source} for H5MSM dataset "
                    f"{dataset.name!r}; expected a unit compatible with {expected!r}."
                ),
                caller="molsysmt.h5msm",
            ) from error
        if reference is not None and not np.allclose(
            converted, reference, rtol=1e-12, atol=0.0
        ):
            raise FormatError(
                reason=(
                    f"Conflicting unit declarations for H5MSM dataset "
                    f"{dataset.name!r}: {declarations!r}."
                ),
                caller="molsysmt.h5msm",
            )
        reference = converted
    return puw.unit(declarations[0][1])


def validate_legacy_structural_units(file):
    """Validate every populated quantity before exposing a legacy file."""
    structures = file.get("structures")
    if structures is None:
        return
    for field in _FIELDS:
        dataset = structures.get(field)
        if dataset is not None and dataset.size:
            legacy_dataset_unit(dataset)
