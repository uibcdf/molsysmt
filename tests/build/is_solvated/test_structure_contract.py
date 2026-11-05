"""Check the water-count/box-volume predicate independently per structure."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentError,
    NotWithThisFormError,
    StructuralInconsistencyError,
)
from molsysmt.native import Structures


def water_system(volumes, n_waters=16, *, with_box=True, unit="nm"):
    """Declare waters; zero coordinates intentionally do not describe liquid water."""
    builder = msm.MolSysBuilder()
    for _ in range(n_waters):
        atoms = [
            builder.add_atom(atom_name=name, atom_type=element)
            for name, element in [("O", "O"), ("H1", "H"), ("H2", "H")]
        ]
        builder.add_group(atoms, group_name="HOH")
        builder.add_bond(atoms[0], atoms[1])
        builder.add_bond(atoms[0], atoms[2])
    if n_waters == 0:
        atom = builder.add_atom(atom_name="C1", atom_type="C")
        builder.add_group([atom], group_name="LIG")
    n_atoms = 3 * n_waters if n_waters else 1
    builder.set_coordinates(puw.quantity(np.zeros((len(volumes), n_atoms, 3)), "nm"))
    if with_box:
        box = np.repeat(np.eye(3)[None], len(volumes), axis=0)
        box[:, 0, 0] = volumes
        builder.set_box(puw.convert(puw.quantity(box, "nm"), to_unit=unit))
    return builder.build()


@pytest.mark.parametrize("n_waters,expected", [(14, False), (15, False), (16, True)])
def test_single_structure_retains_python_boolean_and_strict_threshold(
    n_waters, expected
):
    assert msm.build.is_solvated(water_system([1.0], n_waters)) is expected


@pytest.mark.parametrize(
    "volumes,expected",
    [
        ([1.0, 1.0], [True, True]),
        ([2.0, 2.0], [False, False]),
        ([1.0, 2.0, 1.0], [True, False, True]),
    ],
)
def test_multiple_structures_return_independent_boolean_values(volumes, expected):
    result = msm.build.is_solvated(water_system(volumes))
    assert isinstance(result, np.ndarray)
    assert result.shape == (len(volumes),) and result.dtype == np.dtype(bool)
    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize(
    "indices,expected",
    [(2, True), ([1], False), ([2, 1, 2, 0], [True, False, True, True]), ([], [])],
)
def test_structure_selection_preserves_order_and_repetitions(indices, expected):
    result = msm.build.is_solvated(
        water_system([1.0, 2.0, 1.0]), structure_indices=indices
    )
    if isinstance(expected, bool):
        assert result is expected
    else:
        assert result.dtype == np.dtype(bool) and result.shape == (len(expected),)
        np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize("n_structures", [1, 3])
@pytest.mark.parametrize("missing", ["water", "box"])
def test_absent_prerequisites_are_false_on_the_selected_structure_axis(
    n_structures, missing
):
    source = water_system(
        [1.0] * n_structures,
        n_waters=0 if missing == "water" else 16,
        with_box=missing != "box",
    )
    result = msm.build.is_solvated(source)
    if n_structures == 1:
        assert result is False
    else:
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.dtype(bool) and result.shape == (n_structures,)
        np.testing.assert_array_equal(result, [False] * n_structures)


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_equivalent_units_and_nondefault_policy_preserve_the_predicate(unit):
    source = water_system([1.0, 2.0, 1.0], unit=unit)
    with puw.context(standard_units=["angstrom", "fs", "kcal/mol", "K"]):
        result = msm.build.is_solvated(source)
    np.testing.assert_array_equal(result, [True, False, True])


@pytest.mark.parametrize("form", ["native", "composition", "dictionary", "h5msm"])
def test_available_forms_supply_one_shared_predicate(tmp_path, form):
    source = water_system([1.0, 2.0, 1.0])
    if form == "composition":
        system = [source.topology, source.structures]
    elif form == "dictionary":
        system = msm.convert(source, to_form="molsysmt.MolSysDict")
    elif form == "h5msm":
        system = tmp_path / "water.h5msm"
        msm.convert(source, to_form=str(system))
    else:
        system = source
    np.testing.assert_array_equal(
        msm.build.is_solvated(system, structure_indices=[2, 1, 2]), [True, False, True]
    )


@pytest.mark.parametrize("indices", [[-1], [3], [True], [0.5], [[0]], None])
def test_invalid_indices_are_rejected_even_without_waters(indices):
    with pytest.raises(ArgumentError):
        msm.build.is_solvated(
            water_system([1.0, 2.0], n_waters=0), structure_indices=indices
        )


@pytest.mark.parametrize("volume", [0.0, -1.0, np.nan, np.inf])
def test_nonpositive_or_nonfinite_volume_is_not_a_positive_solvation_claim(volume):
    with pytest.raises(StructuralInconsistencyError, match="volume"):
        msm.build.is_solvated(water_system([volume]))


def test_missing_water_inventory_is_an_explicit_unavailable_attribute():
    source = Structures(box=puw.quantity(np.eye(3)[None], "nm"))
    with pytest.raises(NotWithThisFormError):
        msm.build.is_solvated(source)


def test_reading_preserves_source_and_named_analysis_identity():
    source = water_system([1.0, 2.0, 1.0])
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=source.topology.n_atoms,
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="synthetic.audit",
    )
    source.interactions = {"audit": analysis}
    before = deepcopy(
        (source.structures.get_coordinates(), source.structures.get_box())
    )
    np.testing.assert_array_equal(msm.build.is_solvated(source), [True, False, True])
    np.testing.assert_array_equal(
        puw.get_value(source.structures.get_coordinates(), to_unit="nm"),
        puw.get_value(before[0], to_unit="nm"),
    )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.get_box(), to_unit="nm"),
        puw.get_value(before[1], to_unit="nm"),
    )
    assert source.interactions["audit"] is analysis
    assert analysis.evaluated_structure_indices.tolist() == [0, 1, 2]


def test_legacy_positional_skip_flag_still_has_its_original_meaning():
    assert msm.build.is_solvated(water_system([1.0]), True) is True


def test_density_predicate_does_not_require_coordinates():
    source = water_system([1.0, 2.0, 1.0])
    source.structures = Structures(box=source.structures.box)
    assert source.structures.coordinates is None
    np.testing.assert_array_equal(msm.build.is_solvated(source), [True, False, True])


def test_native_coordinates_are_not_materialized_for_the_density_predicate(monkeypatch):
    source = water_system([1.0, 2.0, 1.0])
    coordinates = source.structures._coordinates
    original = type(coordinates)._dense

    def refuse_coordinates(array, *args, **kwargs):
        if array is coordinates:
            raise AssertionError(
                "The density predicate must not read atomic coordinates."
            )
        return original(array, *args, **kwargs)

    monkeypatch.setattr(type(coordinates), "_dense", refuse_coordinates)
    np.testing.assert_array_equal(msm.build.is_solvated(source), [True, False, True])


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_equality_at_threshold_is_invariant_under_equivalent_length_units(unit):
    assert msm.build.is_solvated(water_system([1.0], n_waters=15, unit=unit)) is False


@pytest.mark.parametrize(
    "density,expected", [(15.0 - 1e-9, False), (15.0 + 1e-9, True)]
)
def test_roundoff_tolerance_does_not_replace_the_density_threshold(density, expected):
    assert (
        msm.build.is_solvated(water_system([15.0 / density], n_waters=15)) is expected
    )
