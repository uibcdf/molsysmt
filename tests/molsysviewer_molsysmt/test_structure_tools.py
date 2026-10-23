"""Receive native geometric tools while preserving physical units and the scene."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm

pytest.importorskip("molsysviewer.system_edits")
puw = msm.pyunitwizard
NAMES = (
    "get_distances",
    "get_vectors",
    "get_center",
    "get_radius_of_gyration",
    "get_angles",
    "get_dihedral_angles",
)
SCOPE = [2, 0, 2]


def same_result(actual, expected):
    assert type(actual) is type(expected)
    if puw.is_quantity(actual):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_allclose(
            puw.get_value(actual), puw.get_value(expected), equal_nan=True
        )
    elif isinstance(actual, dict):
        assert actual.keys() == expected.keys()
        for key in actual:
            same_result(actual[key], expected[key])
    elif isinstance(actual, (tuple, list)):
        assert len(actual) == len(expected)
        for left, right in zip(actual, expected):
            same_result(left, right)
    elif isinstance(actual, np.ndarray):
        assert actual.dtype == expected.dtype
        np.testing.assert_equal(actual, expected)
    else:
        assert actual == expected


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as original:
        with msv.new_view(original.molsys, structure_indices=[0, 8, 3]) as result:
            analysis = msm.Interactions.from_records(
                [],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.structure",
            )
            result.interactions.attach(analysis, name="preserve", assume_aligned=True)
            result.regions.add(selection=[0, 2, 4], tag="source")
            yield result


@pytest.mark.parametrize("name", NAMES)
def test_signatures_native_help_and_digestion(view, name):
    native = inspect.signature(getattr(msm.structure, name))
    expected = list(native.parameters.values())[1:]
    if name == "get_dihedral_angles":
        expected.insert(
            -1,
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            ),
        )
    method = getattr(view.addons.molsysmt.structure, name)
    assert list(inspect.signature(method).parameters.values()) == expected
    assert method.digestion_plan is not None
    assert "current view.molsys" in inspect.getdoc(method)
    assert "not a scene object" in inspect.getdoc(method)
    assert "\nmolecular_system :" not in inspect.getdoc(method)
    assert not hasattr(view.addons.molsysmt, name)
    assert set(dir(view.addons.molsysmt.structure)) == set(NAMES)
    assert not hasattr(view.addons.molsysmt.structure, "translate")
    if name == "get_dihedral_angles":
        assert "flag is not added to scientific **kwargs" in inspect.getdoc(method)


@pytest.mark.parametrize("name", ["get_distances", "get_vectors"])
@pytest.mark.parametrize("pbc", [False, True])
@pytest.mark.parametrize("pairs", [False, True])
def test_endpoints_structure_order_and_periodicity_are_native(view, name, pbc, pairs):
    args = dict(
        selection=[4, 0],
        selection_2=[5, 2],
        structure_indices=SCOPE,
        pairs=pairs,
        pbc=pbc,
        heavy_mode="off",
    )
    expected = getattr(msm.structure, name)(view.molsys, **args)
    actual = getattr(view.addons.molsysmt.structure, name)(**args)
    same_result(actual, expected)
    if not pbc:
        xyz = puw.get_value(
            msm.get(
                view.molsys, element="atom", structure_indices=SCOPE, coordinates=True
            ),
            to_unit="nm",
        )
        displacement = (
            xyz[:, [5, 2]] - xyz[:, [4, 0]]
            if pairs
            else xyz[:, None, [5, 2]] - xyz[:, [4, 0], None]
        )
        oracle = (
            displacement
            if name == "get_vectors"
            else np.linalg.norm(displacement, axis=-1)
        )
        np.testing.assert_allclose(
            puw.get_value(actual, to_unit="nm"), oracle, atol=1e-12
        )


@pytest.mark.parametrize("name", ["get_distances", "get_vectors"])
@pytest.mark.parametrize("output_type", ["numpy.ndarray", "dictionary"])
def test_index_metadata_and_two_explicit_systems_are_not_reinterpreted(
    view, name, output_type
):
    reference = msm.copy(view.molsys)
    xyz = msm.get(reference, element="atom", coordinates=True)
    msm.set(reference, coordinates=xyz + puw.quantity(0.3, "nm"))
    before = puw.get_value(
        msm.get(reference, element="atom", coordinates=True), to_unit="nm"
    ).copy()
    args = dict(
        selection=[4, 0],
        selection_2=[5, 2, 3],
        structure_indices=SCOPE,
        molecular_system_2=reference,
        structure_indices_2=[0, 2, 0],
        pbc=False,
        output_type=output_type,
        output_indices="atom",
        output_structure_indices="structure",
        heavy_mode="off",
    )
    expected = getattr(msm.structure, name)(view.molsys, **args)
    actual = getattr(view.addons.molsysmt.structure, name)(**args)
    same_result(actual, expected)
    np.testing.assert_array_equal(
        puw.get_value(
            msm.get(reference, element="atom", coordinates=True), to_unit="nm"
        ),
        before,
    )


@pytest.mark.parametrize("name", ["get_center", "get_radius_of_gyration"])
@pytest.mark.parametrize("heavy_mode", ["off", "force"])
def test_weighted_geometry_matches_independent_coordinate_reference(
    view, name, heavy_mode
):
    weights = np.array([1.0, 2.0, 3.0])
    args = dict(
        selection=[4, 0, 2],
        structure_indices=SCOPE,
        weights=weights,
        heavy_mode=heavy_mode,
    )
    xyz = puw.get_value(
        msm.get(
            view.molsys,
            element="atom",
            selection=[4, 0, 2],
            structure_indices=SCOPE,
            coordinates=True,
        ),
        to_unit="nm",
    )
    center = np.average(xyz, axis=1, weights=weights)
    expected = (
        center[:, None]
        if name == "get_center"
        else np.sqrt(
            np.average(
                np.sum((xyz - center[:, None]) ** 2, axis=-1), axis=1, weights=weights
            )
        )
    )
    with puw.context(standard_units=["nm", "ps", "radians"]):
        actual = getattr(view.addons.molsysmt.structure, name)(**args)
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="nm"), expected, atol=1e-12
    )
    assert puw.get_unit(actual) == puw.unit("nm")


@pytest.mark.parametrize("weights", [None, "masses", [[1.0, 2.0], [3.0, 1.0]]])
def test_group_centers_and_native_weight_options(view, weights):
    args = dict(
        selection=[[4, 0], [2, 5]],
        weights=weights,
        structure_indices=SCOPE,
        heavy_mode="off",
    )
    same_result(
        view.addons.molsysmt.structure.get_center(**args),
        msm.structure.get_center(view.molsys, **args),
    )


@pytest.mark.parametrize("angle_unit", ["radians", "degrees"])
@pytest.mark.parametrize("pbc", [False, True])
def test_angles_and_named_or_explicit_dihedrals_keep_angle_policy(
    view, angle_unit, pbc
):
    with puw.context(standard_units=["pm", "ps", angle_unit]):
        args = dict(
            triplets=np.array([[0, 1, 2], [2, 3, 4]]),
            structure_indices=SCOPE,
            pbc=pbc,
            use_gpu=False,
        )
        actual = view.addons.molsysmt.structure.get_angles(**args)
        same_result(actual, msm.structure.get_angles(view.molsys, **args))
        assert puw.get_unit(actual) == puw.unit(angle_unit)
        for modes in [
            dict(dihedral_quartets=np.array([[0, 1, 2, 3]])),
            dict(phi=True),
            dict(phi=True, psi=True),
        ]:
            args = dict(structure_indices=SCOPE, pbc=pbc, use_gpu=False, **modes)
            actual = view.addons.molsysmt.structure.get_dihedral_angles(
                **args, skip_digestion=True
            )
            same_result(actual, msm.structure.get_dihedral_angles(view.molsys, **args))
            for item in actual if isinstance(actual, list) else [actual]:
                assert puw.get_unit(item) == puw.unit(angle_unit)


@pytest.mark.parametrize(
    "name", ["get_distances", "get_vectors", "get_center", "get_radius_of_gyration"]
)
def test_forced_routes_and_length_policy_are_forwarded_without_hidden_corrections(
    view, name
):
    # Parity only: native forced-distance endpoints and forced-Rg alternate
    # length units have owning defects #441/#440, not scientific qualification.
    args = dict(selection=[0, 2, 4], structure_indices=SCOPE, heavy_mode="force")
    if name in {"get_distances", "get_vectors"}:
        args.update(selection_2=[1, 3], pbc=False)
    with puw.context(standard_units=["pm", "ps", "degrees"]):
        same_result(
            getattr(view.addons.molsysmt.structure, name)(**args),
            getattr(msm.structure, name)(view.molsys, **args),
        )


def test_vector_dictionary_preserves_empty_and_zero_vector_semantics(view):
    for selection in [[], [0]]:
        args = dict(
            selection=selection,
            selection_2=selection,
            pairs=True,
            structure_indices=SCOPE,
            pbc=False,
            output_type="dictionary",
        )
        expected = msm.structure.get_vectors(view.molsys, **args)
        actual = view.addons.molsysmt.structure.get_vectors(**args)
        same_result(actual, expected)
        if selection:
            np.testing.assert_equal(puw.get_value(actual["vectors"]), 0)
            assert np.isnan(actual["directions"]).all()


@pytest.mark.parametrize(
    "name, args",
    [
        ("get_distances", dict(selection=[0, 1], output_indices="group", pbc=False)),
        ("get_vectors", dict(selection=[0, 1], output_indices="group", pbc=False)),
        ("get_center", dict(selection=[])),
        ("get_center", dict(selection=[0, 1], weights=[1.0, -1.0])),
        ("get_radius_of_gyration", dict(selection=[0, 1], weights=[0.0, 0.0])),
        ("get_angles", dict(triplets=[[0, 1]])),
        ("get_dihedral_angles", dict(no_such_dihedral=True)),
    ],
)
def test_native_rejection_retains_scene_status_and_saved_analyses(view, name, args):
    status = view.addons.molsysmt.get_sync_status()
    state = view.export_state()
    analysis = view.molsys.interactions["preserve"]
    with pytest.raises(Exception) as expected:
        getattr(msm.structure, name)(view.molsys, **args)
    with pytest.raises(type(expected.value)):
        getattr(view.addons.molsysmt.structure, name)(**args)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status
    assert view.molsys.interactions["preserve"] is analysis


@pytest.mark.parametrize("name", NAMES)
def test_readers_do_not_modify_coordinates_box_scene_or_analysis(view, name):
    args = dict(structure_indices=SCOPE)
    if name in {"get_distances", "get_vectors"}:
        args.update(selection=[0, 2], selection_2=[1, 3], pbc=False)
    if name == "get_angles":
        args["triplets"] = [[0, 1, 2]]
    if name == "get_dihedral_angles":
        args["phi"] = True
    before = msm.get(view.molsys, element="atom", coordinates=True, box=True)
    copies = [puw.get_value(item).copy() for item in before]
    state = view.export_state()
    analysis = view.molsys.interactions["preserve"]
    getattr(view.addons.molsysmt.structure, name)(**args)
    for old, current in zip(
        copies, msm.get(view.molsys, element="atom", coordinates=True, box=True)
    ):
        np.testing.assert_array_equal(old, puw.get_value(current))
    assert view.export_state() == state
    assert view.molsys.interactions["preserve"] is analysis


@pytest.mark.parametrize("name", NAMES)
def test_empty_closed_and_primary_override_are_rejected(name):
    args = dict(triplets=[[0, 1, 2]]) if name == "get_angles" else {}
    with msv.MolSysView() as empty:
        bound = getattr(empty.addons.molsysmt.structure, name)
        with pytest.raises(ValueError, match="Load a molecular system"):
            bound(**args)
        with pytest.raises(Exception):
            bound(**args, skip_digestion="yes")
        with pytest.raises(TypeError):
            bound(**args, molecular_system=object(), skip_digestion=True)
    with pytest.raises(RuntimeError, match="closed view"):
        bound(**args, skip_digestion=True)


def test_cached_queries_read_pending_coordinates_and_follow_replacement(view):
    tools = view.addons.molsysmt
    center = tools.structure.get_center
    coords = msm.get(
        view.molsys, element="atom", structure_indices=[2], coordinates=True
    )
    tools.basic.set(
        structure_indices=[2],
        coordinates=coords + puw.quantity(0.5, "nm"),
        update_view=False,
    )
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    same_result(
        center(structure_indices=[2]),
        msm.structure.get_center(view.molsys, structure_indices=[2]),
    )
    assert tools.get_sync_status() == status
    tools.sync_view()
    with msv.demo["dialanine"] as other:
        view.load(other.molsys, mode="replace")
    view.addons.manager.disable("molsysmt")
    same_result(center(), msm.structure.get_center(view.molsys))
