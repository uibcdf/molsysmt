"""Prevent geometry edits from corrupting the shared native structure axis."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import MolSys, Structures

puw = msm.pyunitwizard


def system(domain, *, box=True, analyses=False):
    values = np.arange(18, dtype=float).reshape(3, 2, 3)
    structures = Structures(
        coordinates=puw.quantity(values, "nm"),
        box=puw.quantity(np.repeat(np.eye(3)[None] * 2, 3, axis=0), "nm")
        if box
        else None,
        time=puw.quantity([1, 4, 9], "ps"),
        structure_id=["C", "A", "C"],
    )
    target = (
        structures
        if domain == "structures"
        else MolSys._from_partial_domains(structures=structures)
    )
    if analyses:
        target.interactions = {
            "original": msm.Interactions.from_records(
                [],
                n_atoms=2,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="synthetic.box-alignment",
            )
        }
    return target, target if domain == "structures" else target.structures


@pytest.mark.parametrize(
    "domain,analyses", [("structures", False), ("molsys", False), ("molsys", True)]
)
@pytest.mark.parametrize("route", ["public", "native", "property"])
@pytest.mark.parametrize("old_box", [False, True])
def test_misaligned_box_edit_rejects_before_publication_and_coverage_change(
    domain, analyses, route, old_box
):
    target, structures = system(domain, box=old_box, analyses=analyses)
    before_box = structures._box
    before_coordinates = structures._coordinates
    old = None if not analyses else target.interactions["original"]
    value = puw.quantity(np.eye(3)[None] * 3, "nm")
    with pytest.raises(StructuralInconsistencyError):
        if route == "public":
            msm.set(target, box=value)
        elif route == "native":
            structures.set_box(value=value)
        else:
            structures.box = value
    assert structures._box is before_box
    assert structures._coordinates is before_coordinates
    assert structures.n_structures == 3
    np.testing.assert_array_equal(
        puw.get_value(structures.time, to_unit="ps"), [1, 4, 9]
    )
    assert structures.structure_id.tolist() == ["C", "A", "C"]
    if analyses:
        assert target.interactions["original"] is old
        np.testing.assert_array_equal(old.evaluated_structure_indices, [0, 1, 2])


@pytest.mark.parametrize(
    "domain,analyses", [("structures", False), ("molsys", False), ("molsys", True)]
)
@pytest.mark.parametrize("selected", ["all", [2, 0]])
@pytest.mark.parametrize("unit,scale", [("nm", 1), ("pm", 1000)])
@pytest.mark.parametrize("skip", [False, True])
def test_explicit_box_population_retains_metadata_units_and_untouched_scope(
    domain, analyses, selected, unit, scale, skip
):
    target, structures = system(domain, analyses=analyses)
    previous = structures.copy(deep=False)
    old = target.interactions["original"] if analyses else None
    indices = list(range(3)) if isinstance(selected, str) else selected
    values = np.asarray([np.eye(3) * (i + 4) for i in range(len(indices))])
    expected = puw.get_value(structures.box, to_unit="nm").copy()
    expected[indices] = values
    before_xyz = structures._coordinates
    with puw.context(standard_units=[unit, "ps"]):
        policy = puw.configure.report()
        msm.set(
            target,
            structure_indices=selected,
            box=puw.quantity(values * scale, unit),
            skip_digestion=skip,
        )
        assert puw.configure.report() == policy
    assert structures._coordinates is before_xyz and structures.n_structures == 3
    np.testing.assert_allclose(
        puw.get_value(structures.box, to_unit="nm"), expected, rtol=0, atol=1e-14
    )
    np.testing.assert_array_equal(
        puw.get_value(previous.box, to_unit="nm"),
        np.repeat(np.eye(3)[None] * 2, 3, axis=0),
    )
    np.testing.assert_array_equal(
        puw.get_value(structures.time, to_unit="ps"), [1, 4, 9]
    )
    assert structures.structure_id.tolist() == ["C", "A", "C"]
    if analyses:
        np.testing.assert_array_equal(
            target.interactions["original"].evaluated_structure_indices,
            [] if isinstance(selected, str) else [1],
        )
        np.testing.assert_array_equal(old.evaluated_structure_indices, [0, 1, 2])


@pytest.mark.parametrize("bad_count", [0, 2, 4])
def test_invalid_full_cardinality_refuses_with_or_without_initial_box(bad_count):
    for initial in (False, True):
        target, structures = system("molsys", box=initial)
        before = structures._box
        with pytest.raises(StructuralInconsistencyError):
            msm.set(
                target,
                box=puw.quantity(np.repeat(np.eye(3)[None], bad_count, axis=0), "nm"),
            )
        assert structures._box is before and structures.n_structures == 3


def test_full_clearing_and_empty_selected_noop_keep_axes_and_native_snapshots():
    target, structures = system("molsys", analyses=True)
    original = structures._box
    analysis = target.interactions["original"]
    msm.set(target, structure_indices=[], box=None)
    assert structures._box is original and target.interactions["original"] is analysis
    msm.set(target, box=None)
    assert structures.box is None and structures.n_structures == 3
    np.testing.assert_array_equal(
        target.interactions["original"].evaluated_structure_indices, []
    )
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1, 2])
    msm.set(target, structure_indices=[], box=None)
    assert structures.box is None and structures.n_structures == 3


def test_new_payload_construction_is_strict_and_its_scope_is_not_retained():
    target = Structures()
    target.set_box(value=puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0), "nm"))
    assert target.n_structures == 3 and "_initializing_geometry" not in vars(target)
    with pytest.raises(StructuralInconsistencyError):
        Structures(
            coordinates=puw.quantity(np.zeros((3, 2, 3)), "nm"),
            box=puw.quantity(np.eye(3)[None], "nm"),
        )
    failed = object.__new__(Structures)
    with pytest.raises(StructuralInconsistencyError):
        failed.__init__(
            coordinates=puw.quantity(np.zeros((3, 2, 3)), "nm"),
            box=puw.quantity(np.eye(3)[None], "nm"),
        )
    assert "_initializing_geometry" not in vars(failed)


@pytest.mark.parametrize(
    "domain,analyses", [("structures", False), ("molsys", False), ("molsys", True)]
)
@pytest.mark.parametrize("route", ["public", "native", "property"])
@pytest.mark.parametrize("count", [1, 4])
def test_misaligned_coordinates_reject_without_publishing_or_invalidating(
    domain, analyses, route, count
):
    target, structures = system(domain, analyses=analyses)
    original_xyz, original_box = structures._coordinates, structures._box
    original_analysis = target.interactions["original"] if analyses else None
    value = puw.quantity(np.ones((count, 2, 3)), "nm")
    with pytest.raises(StructuralInconsistencyError):
        if route == "public":
            msm.set(target, coordinates=value)
        elif route == "native":
            structures.set_coordinates(value=value)
        else:
            structures.coordinates = value
    assert structures._coordinates is original_xyz
    assert structures._box is original_box and structures.n_structures == 3
    np.testing.assert_array_equal(
        puw.get_value(structures.time, to_unit="ps"), [1, 4, 9]
    )
    assert structures.structure_id.tolist() == ["C", "A", "C"]
    if analyses:
        assert target.interactions["original"] is original_analysis
        np.testing.assert_array_equal(
            original_analysis.evaluated_structure_indices, [0, 1, 2]
        )


@pytest.mark.parametrize("domain", ["structures", "molsys"])
@pytest.mark.parametrize("selected", ["all", [2, 0]])
@pytest.mark.parametrize("unit,scale", [("nm", 1), ("pm", 1000)])
def test_aligned_coordinate_edits_preserve_other_series_and_snapshot(
    domain, selected, unit, scale
):
    target, structures = system(domain, analyses=domain == "molsys")
    previous = structures.copy(deep=False)
    indices = list(range(3)) if isinstance(selected, str) else selected
    values = np.full((len(indices), 2, 3), 4.0)
    expected = puw.get_value(previous.coordinates, to_unit="nm").copy()
    expected[indices] = values
    box = structures._box
    msm.set(
        target,
        structure_indices=selected,
        coordinates=puw.quantity(values * scale, unit),
    )
    np.testing.assert_allclose(
        puw.get_value(structures.coordinates, to_unit="nm"), expected,
        rtol=0, atol=1e-14,
    )
    np.testing.assert_array_equal(
        puw.get_value(previous.coordinates, to_unit="nm"),
        np.arange(18, dtype=float).reshape(3, 2, 3),
    )
    assert structures._box is box and structures.n_structures == 3
    np.testing.assert_array_equal(
        puw.get_value(structures.time, to_unit="ps"), [1, 4, 9]
    )
    if domain == "molsys":
        np.testing.assert_array_equal(
            target.interactions["original"].evaluated_structure_indices,
            [] if isinstance(selected, str) else [1],
        )
