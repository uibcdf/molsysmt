"""Keep native float64 arithmetic explicit without retiring single-coordinate outputs."""

import warnings
from contextlib import nullcontext

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import PrecisionFallbackWarning
from molsysmt.native import MolSys, Structures


def _system(native_kind="structures"):
    xyz = np.array(
        [
            [
                [0.1, 0.2, 0.3],
                [1.1 + 2**-29, 0.2, 0.3],
                [0.3, 1.4, 0.6],
                [0.2, 0.4, 1.7],
            ],
            [
                [0.3, 0.1, 0.2],
                [1.3 + 2**-28, 0.1, 0.2],
                [0.5, 1.3, 0.5],
                [0.4, 0.3, 1.6],
            ],
            [
                [0.4, 0.3, 0.1],
                [1.4 + 2**-27, 0.3, 0.1],
                [0.6, 1.5, 0.4],
                [0.5, 0.5, 1.5],
            ],
        ]
    )
    structures = Structures(
        coordinates=puw.quantity(xyz, "nm"),
        box=puw.quantity(np.repeat(np.diag([8.0, 9, 10])[None], 3, axis=0), "nm"),
    )
    if native_kind == "structures":
        return structures, xyz
    source = MolSys(n_atoms=4)
    source.structures = structures
    return source, xyz


@pytest.mark.parametrize("native_kind", ["structures", "molsys"])
@pytest.mark.parametrize("mode", ["off", "force"])
@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("pbc", [False, True])
def test_requested_single_distances_use_explicit_float64_arithmetic(
    native_kind, mode, unit, pbc
):
    source, xyz = _system(native_kind)
    expected = np.linalg.norm(xyz[:, :, None] - xyz[:, None, :], axis=-1)[[2, 0]]
    with (
        puw.context(standard_units=[unit, "ps"]),
        msm.configure.context(precision="single", chunk_size=1),
    ):
        with pytest.warns(Warning, match="float64") as caught:
            result = msm.structure.get_distances(
                source, structure_indices=[2, 0], heavy_mode=mode, pbc=pbc
            )
    assert any(type(w.message).__name__ == "PrecisionFallbackWarning" for w in caught)
    observed = puw.get_value(result, to_unit="nm")
    assert observed.dtype == np.float64
    np.testing.assert_allclose(observed, expected, rtol=0, atol=1e-12)
    # The deliberately non-float32-representable coordinates must not be quantized.
    coordinates = (
        source.coordinates
        if native_kind == "structures"
        else source.structures.coordinates
    )
    np.testing.assert_array_equal(puw.get_value(coordinates, to_unit="nm"), xyz)


@pytest.mark.parametrize("native_kind", ["structures", "molsys"])
def test_default_double_calculation_does_not_emit_precision_fallback(native_kind):
    source, xyz = _system(native_kind)
    with (
        msm.configure.context(precision="double"),
        warnings.catch_warnings(record=True) as caught,
    ):
        warnings.simplefilter("always")
        result = msm.structure.get_distances(source, pbc=False)
    assert not caught
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="nm"),
        np.linalg.norm(xyz[:, :, None] - xyz[:, None, :], axis=-1),
        rtol=0,
        atol=1e-12,
    )


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("native_kind", ["quantity", "molsys"])
def test_single_fit_coordinate_publication_remains_available(native_kind, in_place):
    reference = np.array(
        [[[0.1, 0.2, 0.3], [1.3, 0.1, 0.2], [0.4, 1.5, 0.1], [0.2, 0.3, 1.7]]]
    )
    original = reference + [0.7, -0.3, 1.1]
    source = puw.quantity(original.copy(), "nm")
    target = puw.quantity(reference, "nm")
    if native_kind == "molsys":
        item = MolSys(n_atoms=4)
        item.structures.coordinates = source
        source = item
        target_item = MolSys(n_atoms=4)
        target_item.structures.coordinates = target
        target = target_item
    with pytest.warns(Warning, match="float64"):
        returned = msm.structure.least_rmsd_fit(
            source,
            selection_fit="all",
            reference_molecular_system=target,
            reference_selection_fit="all",
            precision="single",
            in_place=in_place,
        )
    result = source if in_place else returned
    assert (returned is None) == in_place
    values = puw.get_value(
        result if native_kind == "quantity" else result.structures.coordinates,
        to_unit="nm",
    )
    assert values.dtype == (
        np.float32 if native_kind == "quantity" and not in_place else np.float64
    )
    np.testing.assert_allclose(values, reference.astype(np.float32), rtol=0, atol=2e-7)
    if not in_place:
        before = source if native_kind == "quantity" else source.structures.coordinates
        np.testing.assert_array_equal(puw.get_value(before, to_unit="nm"), original)


def test_precision_warning_promoted_to_error_prevents_in_place_fitting():
    source, before = _system("molsys")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        with pytest.raises(Warning, match="float64"):
            msm.structure.least_rmsd_fit(
                source, selection_fit="all", precision="single", in_place=True
            )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), before
    )


def _same_result(actual, expected):
    if isinstance(expected, (list, tuple)):
        assert type(actual) is type(expected) and len(actual) == len(expected)
        for a, b in zip(actual, expected):
            _same_result(a, b)
    elif puw.is_quantity(expected):
        np.testing.assert_array_equal(
            puw.get_value(actual, to_unit=puw.get_unit(expected)),
            puw.get_value(expected),
        )
    else:
        np.testing.assert_array_equal(actual, expected)


@pytest.mark.parametrize(
    "operation, options",
    [
        ("get_center", {"selection": "all"}),
        ("get_radius_of_gyration", {"selection": "all"}),
        ("get_angles", {"triplets": [[0, 1, 2]]}),
        ("get_dihedral_angles", {"dihedral_quartets": [[0, 1, 2, 3]]}),
        ("get_rmsd", {"selection": "all", "reference_selection": "all"}),
        ("get_least_rmsd", {"selection": "all", "reference_selection": "all"}),
        ("get_rmsf", {"selection": "all"}),
        ("principal_component_analysis", {"selection": "all"}),
        ("get_contacts", {"selection": "all", "pbc": False}),
    ],
)
def test_shared_preparation_consumers_preserve_double_results(operation, options):
    source, before = _system("molsys")
    function = getattr(msm.structure, operation)
    with msm.configure.context(precision="double"):
        expected = function(source, **options)
    with (
        msm.configure.context(precision="single"),
        pytest.warns(Warning, match="float64"),
    ):
        actual = function(source, **options)
    # This is execution parity; independent scientific truth has its own registry.
    _same_result(actual, expected)
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), before
    )


@pytest.mark.parametrize("precision", ["double", "single"])
def test_canonical_working_coordinates_do_not_add_a_dtype_copy(precision):
    from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit

    original = puw.quantity(np.arange(12.0).reshape(1, 4, 3), "nm")
    notice = (
        pytest.warns(PrecisionFallbackWarning)
        if precision == "single"
        else nullcontext()
    )
    with notice, msm.configure.context(precision=precision):
        values, unit = extract_coordinates_value_and_unit(original)
    assert values.dtype == np.float64
    assert np.shares_memory(values, puw.get_value(original))
    assert puw.check(unit, dimensionality={"[L]": 1})


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_two_source_alignment_keeps_coordinate_units_and_native_precision(unit):
    _, xyz = _system()
    shift = np.array([0.2, -0.3, 0.1])
    source = puw.quantity(xyz[:1], "nm")
    reference = puw.quantity((xyz[:1] + shift) * 10, "angstrom")
    with (
        puw.context(standard_units=[unit, "ps"]),
        msm.configure.context(precision="single"),
    ):
        with pytest.warns(PrecisionFallbackWarning):
            result = msm.structure.get_rmsd(
                source,
                selection="all",
                reference_molecular_system=reference,
                reference_selection="all",
            )
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="nm"), np.linalg.norm(shift), rtol=0, atol=1e-12
    )


def test_precision_alias_is_normalized_at_the_configuration_boundary():
    with msm.configure.context(precision="FLOAT32"):
        assert msm.configure.precision == "single"
    with pytest.raises(msm.ArgumentError):
        with msm.configure.context(precision="half"):
            pytest.fail("Unsupported precision was published.")


def test_native_sasa_keeps_its_double_result_under_a_single_request():
    _, xyz = _system()
    builder = msm.MolSysBuilder()
    atoms = [builder.add_atom(atom_name="C" + str(i), atom_type="C") for i in range(4)]
    builder.add_group(atoms, group_name="MOL")
    builder.set_coordinates(puw.quantity(xyz, "nm"))
    source = builder.build()
    with msm.configure.context(precision="double"):
        expected = msm.physchem.get_sasa(source, engine="MolSysMT", pbc=False)
    with (
        msm.configure.context(precision="single"),
        pytest.warns(PrecisionFallbackWarning),
    ):
        actual = msm.physchem.get_sasa(source, engine="MolSysMT", pbc=False)
    _same_result(actual, expected)


def test_explicit_torsion_edit_keeps_double_coordinates_and_input_independence():
    source, original = _system("molsys")
    options = dict(
        dihedral_quartets=[[0, 1, 2, 3]],
        blocks=[[3]],
        angles=puw.quantity(0.7, "radian"),
        pbc=False,
        in_place=False,
    )
    with msm.configure.context(precision="double"):
        expected = msm.structure.set_dihedral_angles(source, **options)
    with (
        msm.configure.context(precision="single"),
        pytest.warns(PrecisionFallbackWarning),
    ):
        actual = msm.structure.set_dihedral_angles(source, **options)
    np.testing.assert_array_equal(
        puw.get_value(actual.structures.coordinates),
        puw.get_value(expected.structures.coordinates),
    )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), original
    )
