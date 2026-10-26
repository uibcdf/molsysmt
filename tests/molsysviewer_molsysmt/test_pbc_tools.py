"""Receive box utilities against metric geometry and native public contracts."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm

puw = msm.pyunitwizard
NAMES = (
    "has_pbc",
    "get_lengths_from_box",
    "get_angles_from_box",
    "get_lengths_and_angles_from_box",
    "get_volume_from_box",
    "get_shape_from_box",
    "get_shape_from_angles",
    "get_volume_from_lengths_and_angles",
    "get_box_from_lengths_and_angles",
    "get_box_with_shape",
)
NO_NATIVE_SKIP = {"get_volume_from_box", "get_volume_from_lengths_and_angles"}


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            yield result


@pytest.fixture
def boxes():
    return np.array(
        [
            [[2.0, 0, 0], [0.3, 2.4, 0], [-0.2, 0.5, 3.1]],
            [[1.5, 0, 0], [0, 2.2, 0], [0, 0, 2.7]],
            [[3.0, 0, 0], [0.6, 2.0, 0], [0.2, -0.3, 2.5]],
        ]
    )


def values(quantity, unit):
    return puw.get_value(quantity, to_unit=unit)


def metric(boxes):
    lengths = np.linalg.norm(boxes, axis=-1)
    pairs = [(1, 2), (0, 2), (0, 1)]
    angles = np.stack(
        [
            np.arccos(
                np.clip(
                    np.sum(boxes[:, i] * boxes[:, j], axis=-1)
                    / (lengths[:, i] * lengths[:, j]),
                    -1,
                    1,
                )
            )
            for i, j in pairs
        ],
        axis=-1,
    )
    return lengths, angles


@pytest.mark.parametrize("name", NAMES)
def test_public_signature_validation_and_binding_help(view, name):
    native = inspect.signature(getattr(msm.pbc, name))
    method = getattr(view.addons.molsysmt.pbc, name)
    expected = list(native.parameters.values())
    if name == "has_pbc":
        expected = expected[1:]
    if name in NO_NATIVE_SKIP:
        expected.append(
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            )
        )
    assert inspect.signature(method) == native.replace(parameters=expected)
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, name)
    assert "update_view" not in inspect.signature(method).parameters
    doc = inspect.getdoc(method)
    assert "Native unit policy" in doc
    if name == "has_pbc":
        assert "current view.molsys" in doc and "first structure" in doc
        assert "\nmolecular_system :" not in doc
    else:
        assert "explicit scientific inputs" in doc
        assert "The primary molecular system is the current" not in doc
    if name in NO_NATIVE_SKIP:
        assert "retains ordinary validation" in doc


def test_namespace_has_explicit_queries_and_factories_only(view):
    assert set(dir(view.addons.molsysmt.pbc)) == set(NAMES)
    assert "pbc" in dir(view.addons.molsysmt)
    native = {
        n
        for n, f in vars(msm.pbc).items()
        if not n.startswith("_") and inspect.isfunction(f)
    }
    assert native - set(NAMES) == {"wrap_to_pbc", "wrap_to_mic", "unwrap"}
    for name in native - set(NAMES):
        assert not hasattr(view.addons.molsysmt.pbc, name)


@pytest.mark.parametrize(
    "length_unit,angle_unit",
    [
        ("nm", "radians"),
        ("angstrom", "degrees"),
        ("pm", "degrees"),
    ],
)
def test_geometry_uses_rows_units_and_nonconsecutive_repeated_boxes(
    view,
    boxes,
    length_unit,
    angle_unit,
):
    tools = view.addons.molsysmt
    msm.set(view.molsys, box=puw.quantity(boxes, "nm"))
    state, status = view.export_state(), tools.get_sync_status()
    selected = tools.basic.get(box=True, structure_indices=[2, 0, 2])
    before = values(selected, "nm").copy()
    expected_lengths, expected_angles = metric(boxes[[2, 0, 2]])
    with puw.context(standard_units=[length_unit, "ps", angle_unit]):
        box = puw.convert(selected, to_unit=length_unit)
        lengths, angles = tools.pbc.get_lengths_and_angles_from_box(box)
        np.testing.assert_allclose(values(lengths, "nm"), expected_lengths, atol=6e-7)
        np.testing.assert_allclose(
            values(angles, "radians"), expected_angles, atol=6e-7
        )
        assert puw.get_unit(lengths) == puw.unit(length_unit)
        assert puw.get_unit(angles) == puw.unit(angle_unit)
        np.testing.assert_allclose(
            values(tools.pbc.get_lengths_from_box(box), "nm"),
            expected_lengths,
            atol=6e-7,
        )
        np.testing.assert_allclose(
            values(tools.pbc.get_angles_from_box(box), "radians"),
            expected_angles,
            atol=6e-7,
        )
        volume = tools.pbc.get_volume_from_box(box)
        np.testing.assert_allclose(
            values(volume, "nm**3"), np.linalg.det(before), atol=1e-12
        )
        # This native helper keeps nm cubed rather than standardizing the result.
        assert puw.get_unit(volume) == puw.unit("nm**3")
        rebuilt = tools.pbc.get_box_from_lengths_and_angles(lengths, angles)
        np.testing.assert_allclose(values(rebuilt, "nm"), before, atol=4e-6)
        via_angles = tools.pbc.get_volume_from_lengths_and_angles(lengths, angles)
        np.testing.assert_allclose(
            values(via_angles, "nm**3"), np.linalg.det(before), rtol=3e-6
        )
        for name, arguments in [
            ("get_lengths_from_box", (box,)),
            ("get_angles_from_box", (box,)),
            ("get_volume_from_box", (box,)),
            ("get_box_from_lengths_and_angles", (lengths, angles)),
            ("get_volume_from_lengths_and_angles", (lengths, angles)),
        ]:
            actual = getattr(tools.pbc, name)(*arguments)
            expected = getattr(msm.pbc, name)(*arguments)
            assert type(actual) is type(expected)
            assert puw.get_unit(actual) == puw.get_unit(expected)
            np.testing.assert_array_equal(
                puw.get_value(actual), puw.get_value(expected)
            )
    np.testing.assert_array_equal(values(selected, "nm"), before)
    assert view.export_state() == state and tools.get_sync_status() == status


@pytest.mark.parametrize(
    "shape,volume_factor",
    [
        ("cubic", 1.0),
        ("truncated octahedral", 4 / (3 * np.sqrt(3))),
        ("rhombic dodecahedral", 1 / np.sqrt(2)),
    ],
)
@pytest.mark.parametrize("length_unit", ["nm", "angstrom", "pm"])
def test_factories_preserve_metric_without_assigning_a_system_box(
    shape, volume_factor, length_unit
):
    with msv.new_view() as view:
        pbc = view.addons.molsysmt.pbc
        with puw.context(standard_units=[length_unit, "ps", "radians"]):
            box = pbc.get_box_with_shape(shape=shape, length="2 nm", n_structures=3)
            v = values(box, "nm")
            assert v.shape == (3, 3, 3)
            assert puw.get_unit(box) == puw.unit(length_unit)
            np.testing.assert_allclose(np.linalg.norm(v, axis=-1), 2, atol=1e-12)
            np.testing.assert_allclose(np.linalg.det(v), 8 * volume_factor, atol=1e-12)
            assert pbc.get_shape_from_box(box) == shape
            assert pbc.get_shape_from_angles(pbc.get_angles_from_box(box)) == shape
            assert view.molsys is None


def test_default_factory_and_explicit_factories_before_load():
    with msv.new_view() as view:
        pbc = view.addons.molsysmt.pbc
        np.testing.assert_array_equal(
            values(pbc.get_box_with_shape(), "nm"), [np.eye(3)]
        )
        lengths = puw.quantity([[2, 3, 4], [3, 4, 5]], "nm")
        angles = puw.quantity([[90, 90, 90], [90, 90, 60]], "degrees")
        box = pbc.get_box_from_lengths_and_angles(lengths, angles)
        np.testing.assert_allclose(values(box, "nm")[0], np.diag([2, 3, 4]), atol=1e-6)
        # Direct volume uses unrounded geometry, independently of box reconstruction.
        volume = pbc.get_volume_from_lengths_and_angles(lengths, angles)
        np.testing.assert_allclose(
            values(volume, "nm**3"), [24, 60 * np.sqrt(3) / 2], atol=1e-12
        )
        with pytest.raises(ValueError, match="Load a molecular system"):
            pbc.has_pbc()
        assert view.molsys is None


def test_shape_classification_keeps_native_mean_angle_semantics():
    with msv.new_view() as view:
        pbc = view.addons.molsysmt.pbc
        # Orthorhombic unequal lengths still receive native's angle-based cubic label.
        assert (
            pbc.get_shape_from_box(puw.quantity([np.diag([2, 3, 4])], "nm")) == "cubic"
        )
        assert (
            pbc.get_shape_from_angles(puw.quantity([[80, 90, 100]], "degrees"))
            == "triclinic"
        )
        assert (
            pbc.get_shape_from_angles(
                puw.quantity([[80, 90, 100], [100, 90, 80]], "degrees")
            )
            == "cubic"
        )
        assert pbc.get_shape_from_box(None) is None
        assert pbc.get_volume_from_box(None) is None


def test_has_pbc_observes_pending_box_edits_and_cached_facade(view, boxes):
    tools = view.addons.molsysmt
    pbc = tools.pbc
    msm.set(view.molsys, box=None)
    assert pbc.has_pbc() is False
    tools.basic.set(box=puw.quantity(boxes, "nm"), update_view=False)
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    assert pbc.has_pbc() is True and msm.pbc.has_pbc(view.molsys) is True
    assert tools.get_sync_status() == status
    assert status["pending_operations"] == 1
    tools.sync_view()
    assert tools.get_sync_status()["state"] == "synchronized"
    tools.basic.set(box=None, update_view=False)
    assert pbc.has_pbc() is False
    tools.sync_view()


@pytest.mark.parametrize("skip", [False, True])
def test_addon_only_skip_keeps_native_validation_and_closed_view_guards(skip):
    with msv.new_view() as view:
        pbc = view.addons.molsysmt.pbc
        for name, arguments in [
            ("get_volume_from_box", {"box": puw.quantity([np.eye(3)], "ps")}),
            (
                "get_volume_from_lengths_and_angles",
                {
                    "box_lengths": puw.quantity([[2, 3, 4]], "ps"),
                    "box_angles": puw.quantity([[90, 90, 90]], "degrees"),
                },
            ),
        ]:
            with pytest.raises(Exception) as native_error:
                getattr(msm.pbc, name)(**arguments)
            with pytest.raises(type(native_error.value)):
                getattr(pbc, name)(**arguments, skip_digestion=skip)
    with pytest.raises(RuntimeError, match="closed view"):
        pbc.get_box_with_shape(skip_digestion=skip)
    with pytest.raises(RuntimeError, match="closed view"):
        pbc.has_pbc(skip_digestion=skip)


@pytest.mark.parametrize(
    "name,arguments",
    [
        ("get_box_with_shape", {"shape": "unknown"}),
        ("get_lengths_from_box", {"box": puw.quantity(np.ones((2, 2)), "nm")}),
        (
            "get_box_from_lengths_and_angles",
            {
                "box_lengths": puw.quantity([[2, 3, 4]], "nm"),
                "box_angles": puw.quantity([[90, 90, 90]], "ps"),
            },
        ),
    ],
)
def test_explicit_input_rejections_are_native_without_scene_effects(
    view, name, arguments
):
    state = view.export_state()
    with pytest.raises(Exception) as native_error:
        getattr(msm.pbc, name)(**arguments)
    with pytest.raises(type(native_error.value)):
        getattr(view.addons.molsysmt.pbc, name)(**arguments)
    assert view.export_state() == state


@pytest.mark.parametrize("skip", [False, True])
def test_primary_cannot_be_overridden_and_query_has_no_implicit_structure_filter(
    view, skip
):
    with pytest.raises((TypeError, UnknownArgumentError)):
        view.addons.molsysmt.pbc.has_pbc(
            molecular_system=view.molsys, skip_digestion=skip
        )
    with pytest.raises((TypeError, UnknownArgumentError)):
        view.addons.molsysmt.pbc.has_pbc(structure_indices=[2, 0], skip_digestion=skip)
