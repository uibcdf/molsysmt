"""Protecting unit integrity across all legacy H5MSM read routes."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError
from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm
from molsysmt.native import H5MSMFileHandler, MolSys, Structures

_FIELDS = {
    "coordinates": ("angstrom", "nm", 0.1, "length_unit"),
    "box": ("angstrom", "nm", 0.1, "length_unit"),
    "velocities": ("angstrom/fs", "nm/ps", 100.0, "velocity_unit"),
    "b_factor": ("angstrom**2", "nm**2", 0.01, "b_factor_unit"),
    "time": ("fs", "ps", 0.001, "time_unit"),
    "temperature": ("mK", "K", 0.001, "temperature_unit"),
    "potential_energy": ("kcal/mol", "kJ/mol", 4.184, "energy_unit"),
    "kinetic_energy": ("kcal/mol", "kJ/mol", 4.184, "energy_unit"),
}


@pytest.fixture
def legacy_file(tmp_path):
    puw = msm.pyunitwizard
    structures = Structures(
        coordinates=puw.quantity(np.ones((2, 2, 3)), "nm"),
        box=puw.quantity(np.repeat(np.eye(3)[None], 2, axis=0), "nm"),
        velocities=puw.quantity(np.ones((2, 2, 3)), "nm/ps"),
        b_factor=puw.quantity(np.ones((2, 2)), "nm**2"),
        time=puw.quantity(np.array([1.0, 2.0]), "ps"),
        temperature=puw.quantity(np.full(2, 300.0), "K"),
        potential_energy=puw.quantity(np.ones(2), "kJ/mol"),
        kinetic_energy=puw.quantity(np.ones(2), "kJ/mol"),
        skip_digestion=True,
    )
    path = tmp_path / "legacy.h5msm"
    molsys = MolSys(n_atoms=2)
    molsys.structures = structures
    to_file_h5msm(molsys, output_filename=path)
    return path


def _read(path, route, field):
    if route == "get":
        return msm.get(path, **{field: True})
    if route == "convert":
        return msm.get(
            msm.convert(path, to_form="molsysmt.Structures"), **{field: True}
        )
    if route == "iterator":
        handler = H5MSMFileHandler(path)
        try:
            return next(msm.Iterator(handler, chunk=2, **{field: True}))
        finally:
            handler.close()
    migrated = path.with_name("migrated.h5msm")
    msm.h5msm.migrate_04_to_05(path, migrated)
    return msm.get(migrated, **{field: True})


@pytest.mark.parametrize("route", ["get", "convert", "iterator", "migrate"])
def test_conflicting_units_rejected_by_every_route(legacy_file, route):
    with h5py.File(legacy_file, "r+") as file:
        file["structures/coordinates"].attrs["unit"] = "angstrom"
    with pytest.raises(FormatError, match="Conflicting unit declarations"):
        _read(legacy_file, route, "coordinates")


@pytest.mark.parametrize("field", list(_FIELDS))
@pytest.mark.parametrize("route", ["get", "convert", "migrate"])
def test_dataset_only_units_preserve_physical_values(legacy_file, field, route):
    unit, target, scale, _ = _FIELDS[field]
    with h5py.File(legacy_file, "r+") as file:
        for owner in (file, file["structures"]):
            for key in list(owner.attrs):
                if key.endswith("_unit"):
                    del owner.attrs[key]
        for name, (_, canonical, _, _) in _FIELDS.items():
            file[f"structures/{name}"].attrs["unit"] = canonical
        file[f"structures/{field}"].attrs["unit"] = unit
        file[f"structures/{field}"][:] = 1.0
    result = _read(legacy_file, route, field)
    assert msm.pyunitwizard.check(result, unit=target)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit=target), scale
    )


@pytest.mark.parametrize("route", ["get", "convert", "iterator", "migrate"])
def test_missing_units_are_never_guessed(legacy_file, route):
    with h5py.File(legacy_file, "r+") as file:
        del file["structures/coordinates"].attrs["unit"]
        del file.attrs["length_unit"]
        del file["structures"].attrs["length_unit"]
    with pytest.raises(FormatError, match="no explicit unit declaration"):
        _read(legacy_file, route, "coordinates")


@pytest.mark.parametrize("unit", ["ps", "not_a_real_unit", ""])
def test_invalid_or_wrong_dimension_unit_rejected(legacy_file, unit):
    with h5py.File(legacy_file, "r+") as file:
        file["structures/coordinates"].attrs["unit"] = unit
    with pytest.raises(FormatError, match="Invalid unit"):
        msm.get(legacy_file, coordinates=True)


@pytest.mark.parametrize("route", ["get", "convert", "iterator", "migrate"])
def test_equivalent_units_follow_nondefault_session_policy(legacy_file, route):
    with h5py.File(legacy_file, "r+") as file:
        file.attrs["length_unit"] = "nm"
        file["structures"].attrs["length_unit"] = "nanometer"
        file["structures/coordinates"].attrs["unit"] = np.bytes_("nanometers")
    with msm.pyunitwizard.context(standard_units=["angstrom", "fs"]):
        result = _read(legacy_file, route, "coordinates")
        assert msm.pyunitwizard.check(result, unit="angstrom")
        np.testing.assert_allclose(msm.pyunitwizard.get_value(result), 10.0)


@pytest.mark.parametrize("field", ["coordinates", "box", "time"])
def test_iterator_uses_dataset_unit_without_root_metadata(legacy_file, field):
    with h5py.File(legacy_file, "r+") as file:
        for owner in (file, file["structures"]):
            for key in list(owner.attrs):
                if key.endswith("_unit"):
                    del owner.attrs[key]
        for name, (_, canonical, _, _) in _FIELDS.items():
            file[f"structures/{name}"].attrs["unit"] = canonical
        unit, target, scale, _ = _FIELDS[field]
        file[f"structures/{field}"].attrs["unit"] = unit
        file[f"structures/{field}"][:] = 1.0
    result = _read(legacy_file, "iterator", field)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit=target), scale
    )


@pytest.mark.parametrize("location", ["root", "group"])
def test_explicit_legacy_container_units_remain_supported(legacy_file, location):
    with h5py.File(legacy_file, "r+") as file:
        for name in _FIELDS:
            if "unit" in file[f"structures/{name}"].attrs:
                del file[f"structures/{name}"].attrs["unit"]
        if location == "root":
            file.attrs["b_factor_unit"] = file["structures"].attrs["b_factor_unit"]
        removed = file["structures"] if location == "root" else file
        for key in list(removed.attrs):
            if key.endswith("_unit"):
                del removed.attrs[key]
    for field, (_, target, _, _) in _FIELDS.items():
        direct = msm.get(legacy_file, **{field: True})
        converted = getattr(
            msm.convert(legacy_file, to_form="molsysmt.Structures"), field
        )
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(direct, to_unit=target),
            msm.pyunitwizard.get_value(converted, to_unit=target),
        )


def test_conflicting_container_units_rejected_without_dataset_unit(legacy_file):
    with h5py.File(legacy_file, "r+") as file:
        del file["structures/coordinates"].attrs["unit"]
        file["structures"].attrs["length_unit"] = "angstrom"
    with pytest.raises(FormatError, match="Conflicting unit declarations"):
        msm.get(legacy_file, coordinates=True)


def test_missing_b_factor_unit_is_not_inferred_from_coordinate_unit(legacy_file):
    with h5py.File(legacy_file, "r+") as file:
        file["structures/b_factor"].attrs.pop("unit", None)
        file["structures"].attrs.pop("b_factor_unit", None)
        file.attrs.pop("b_factor_unit", None)
        assert "length_unit" in file.attrs
    with pytest.raises(FormatError, match="no explicit unit declaration"):
        msm.get(legacy_file, b_factor=True)
