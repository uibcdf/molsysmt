"""Protecting validated structure-aligned temperature and energy inputs."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentError,
    ArgumentLengthError,
    StructuralInconsistencyError,
)
from molsysmt.native import Structures

OBSERVABLES = [
    ("temperature", "mK", [300000.0, 301000.0, 302000.0], "K", [300.0, 301.0, 302.0]),
    (
        "potential_energy",
        "kcal/mol",
        [-1.0, -2.0, -3.0],
        "kJ/mol",
        [-4.184, -8.368, -12.552],
    ),
    ("kinetic_energy", "kcal/mol", [0.1, 0.2, 0.3], "kJ/mol", [0.4184, 0.8368, 1.2552]),
]


def _coordinates(n_structures):
    return puw.quantity(np.arange(n_structures * 6).reshape(n_structures, 2, 3), "nm")


@pytest.mark.parametrize("name,input_unit,values,unit,expected", OBSERVABLES)
def test_constructor_accepts_and_queries_structure_series(
    name, input_unit, values, unit, expected
):
    molsys = Structures(
        coordinates=_coordinates(3), **{name: puw.quantity(values, input_unit)}
    )
    assert molsys.n_structures == 3 and molsys.n_atoms == 2
    query = molsys.get(structure_indices=[2, 0, 2], **{name: True})
    assert query.shape == (3,)
    np.testing.assert_allclose(
        puw.get_value(query, to_unit=unit), np.array(expected)[[2, 0, 2]]
    )
    np.testing.assert_allclose(
        puw.get_value(msm.get(molsys, **{name: True}), to_unit=unit), expected
    )


@pytest.mark.parametrize("name,input_unit,values,unit,expected", OBSERVABLES)
def test_append_preserves_selected_observable_order(
    name, input_unit, values, unit, expected
):
    molsys = Structures(
        coordinates=_coordinates(1), **{name: puw.quantity(values[:1], input_unit)}
    )
    molsys.append(
        coordinates=_coordinates(3),
        structure_indices=[2, 0, 2],
        attribute_policy="strict",
        **{name: puw.quantity(values, input_unit)},
    )
    assert molsys.n_structures == 4
    np.testing.assert_allclose(
        puw.get_value(getattr(molsys, name), to_unit=unit),
        np.array(expected)[[0, 2, 0, 2]],
    )


@pytest.mark.parametrize("name,input_unit,values,unit,expected", OBSERVABLES)
def test_scalar_is_one_structure_and_is_not_broadcast(
    name, input_unit, values, unit, expected
):
    value = puw.quantity(values[0], input_unit)
    molsys = Structures(coordinates=_coordinates(1), **{name: value})
    assert getattr(molsys, name).shape == (1,)
    molsys.append(coordinates=_coordinates(1), **{name: value})
    np.testing.assert_allclose(
        puw.get_value(getattr(molsys, name), to_unit=unit), [expected[0]] * 2
    )
    with pytest.raises(StructuralInconsistencyError):
        Structures(coordinates=_coordinates(2), **{name: value})


@pytest.mark.parametrize("name,input_unit,values,unit,expected", OBSERVABLES)
def test_observable_only_and_empty_objects(name, input_unit, values, unit, expected):
    molsys = Structures(**{name: puw.quantity(values, input_unit)})
    assert molsys.n_structures == 3 and molsys.n_atoms == 0
    assert molsys.coordinates is None
    empty = Structures(**{name: puw.quantity(np.empty(0), input_unit)})
    assert empty.n_structures == 0
    assert getattr(empty, name).shape == (0,)
    assert Structures(**{name: None}).n_structures == 0


@pytest.mark.parametrize("name,input_unit,values,unit,expected", OBSERVABLES)
@pytest.mark.parametrize("bad", ["bare", "dimensions", "matrix", "complex", "boolean"])
def test_invalid_series_rejected_without_mutating_append(
    name, input_unit, values, unit, expected, bad
):
    candidates = {
        "bare": values,
        "dimensions": puw.quantity(values, "nm"),
        "matrix": puw.quantity(np.array(values)[:, None], input_unit),
        "complex": puw.quantity(np.array(values, dtype=complex), input_unit),
        "boolean": puw.quantity([True, False, True], input_unit),
    }
    with pytest.raises(ArgumentError):
        Structures(coordinates=_coordinates(3), **{name: candidates[bad]})
    molsys = Structures(
        coordinates=_coordinates(1), **{name: puw.quantity(values[:1], input_unit)}
    )
    before = puw.get_value(getattr(molsys, name), to_unit=unit).copy()
    with pytest.raises(ArgumentError):
        molsys.append(coordinates=_coordinates(3), **{name: candidates[bad]})
    assert molsys.n_structures == 1
    np.testing.assert_array_equal(
        puw.get_value(getattr(molsys, name), to_unit=unit), before
    )


@pytest.mark.parametrize("name,input_unit,values,unit,expected", OBSERVABLES)
def test_length_mismatch_is_atomic(name, input_unit, values, unit, expected):
    with pytest.raises(StructuralInconsistencyError):
        Structures(
            coordinates=_coordinates(2), **{name: puw.quantity(values, input_unit)}
        )
    molsys = Structures(
        coordinates=_coordinates(1), **{name: puw.quantity(values[:1], input_unit)}
    )
    before = puw.get_value(molsys.coordinates, to_unit="nm").copy()
    with pytest.raises(ArgumentLengthError):
        molsys.append(
            coordinates=_coordinates(2), **{name: puw.quantity(values, input_unit)}
        )
    assert molsys.n_structures == 1
    np.testing.assert_array_equal(
        puw.get_value(molsys.coordinates, to_unit="nm"), before
    )
    np.testing.assert_allclose(
        puw.get_value(getattr(molsys, name), to_unit=unit), expected[:1]
    )


def test_nondefault_unit_policy_and_inherited_boundary():
    class Ensemble(Structures):
        pass

    with puw.context(standard_units=["nm", "ps", "mK", "kcal/mol"]):
        molsys = Ensemble(
            coordinates=_coordinates(2),
            temperature=puw.quantity([300.0, 301.0], "K"),
            potential_energy=puw.quantity([-4.184, -8.368], "kJ/mol"),
        )
        molsys.append(
            coordinates=_coordinates(1),
            temperature=puw.quantity(302.0, "K"),
            potential_energy=puw.quantity(-12.552, "kJ/mol"),
        )
        temperature, energy = molsys.get(temperature=True, potential_energy=True)
        assert puw.has_unit(temperature, "mK")
        assert puw.has_unit(energy, "kcal/mol")
        np.testing.assert_allclose(puw.get_value(temperature), [300000, 301000, 302000])
        np.testing.assert_allclose(puw.get_value(energy), [-1, -2, -3])


@pytest.mark.parametrize("target", ["molsysmt.StructuresDict", "file:h5msm"])
def test_public_roundtrip_preserves_observables_and_units(target, tmp_path):
    with puw.context(standard_units=["nm", "ps", "mK", "kcal/mol"]):
        molsys = Structures(
            coordinates=_coordinates(3),
            **{
                name: puw.quantity(values, input_unit)
                for name, input_unit, values, _, _ in OBSERVABLES
            },
        )
        kwargs = (
            {"output_filename": str(tmp_path / "observables.h5msm")}
            if target.startswith("file:")
            else {}
        )
        stored = msm.convert(molsys, to_form=target, **kwargs)
        restored = msm.convert(
            stored, to_form="molsysmt.Structures", structure_indices=[2, 0, 2]
        )
        assert restored.n_structures == 3 and restored.n_atoms == 2
        for name, _, _, unit, expected in OBSERVABLES:
            output = restored.get(**{name: True})
            assert output.shape == (3,)
            np.testing.assert_allclose(
                puw.get_value(output, to_unit=unit), np.array(expected)[[2, 0, 2]]
            )


@pytest.mark.parametrize("name,input_unit,values,unit,expected", OBSERVABLES)
def test_native_alignment_refuses_malformed_stored_observables(
    name, input_unit, values, unit, expected
):
    source = Structures(coordinates=_coordinates(3))
    setattr(source, name, puw.quantity(np.array(values)[:, None], input_unit))
    target = Structures(
        coordinates=_coordinates(1), **{name: puw.quantity(values[:1], input_unit)}
    )
    with pytest.raises(StructuralInconsistencyError):
        target.append_structures(source)
    assert target.n_structures == 1
    np.testing.assert_allclose(
        puw.get_value(getattr(target, name), to_unit=unit), expected[:1]
    )
    with pytest.raises(StructuralInconsistencyError):
        _ = source.n_structures
