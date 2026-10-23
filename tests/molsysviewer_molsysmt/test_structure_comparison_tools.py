"""Receive independent structural queries without distance routing or scene edits."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm

pytest.importorskip("molsysviewer.system_edits")
puw = msm.pyunitwizard
NAMES = ("get_rmsd", "get_least_rmsd", "get_principal_axes", "get_least_squares_plane")
PREVIOUS = (
    "get_distances",
    "get_vectors",
    "get_center",
    "get_radius_of_gyration",
    "get_angles",
    "get_dihedral_angles",
)
SCOPE = [2, 0, 2]
ATOMS = [0, 10, 25, 40, 55]


def assert_native(actual, expected):
    assert type(actual) is type(expected)
    if puw.is_quantity(actual):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_allclose(
            puw.get_value(actual), puw.get_value(expected), equal_nan=True
        )
    elif isinstance(actual, dict):
        assert actual.keys() == expected.keys()
        for key in actual:
            assert_native(actual[key], expected[key])
    elif isinstance(actual, (list, tuple)):
        assert len(actual) == len(expected)
        for left, right in zip(actual, expected):
            assert_native(left, right)
    elif isinstance(actual, np.ndarray):
        assert actual.dtype == expected.dtype
        np.testing.assert_equal(actual, expected)
    else:
        assert actual == expected


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            analysis = msm.Interactions.from_records(
                [],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.structure.comparison",
            )
            result.interactions.attach(analysis, name="preserve", assume_aligned=True)
            result.regions.add(selection=[0, 2, 4], tag="source")
            yield result


@pytest.mark.parametrize("name", NAMES)
def test_explicit_namespace_native_signature_help_and_digestion(view, name):
    native = inspect.signature(getattr(msm.structure, name))
    expected = list(native.parameters.values())[1:]
    if name == "get_rmsd":
        expected.append(
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            )
        )
    bound = getattr(view.addons.molsysmt.structure, name)
    assert list(inspect.signature(bound).parameters.values()) == expected
    assert bound.digestion_plan is not None
    assert "not a scene object" in inspect.getdoc(bound)
    assert "\nmolecular_system :" not in inspect.getdoc(bound)
    assert set(dir(view.addons.molsysmt.structure)) == set(NAMES + PREVIOUS)
    assert not hasattr(view.addons.molsysmt, name)
    assert not hasattr(view.addons.molsysmt.structure, "least_rmsd_fit")
    assert not hasattr(view.addons.molsysmt.structure, "get_rmsf")
    if name == "get_rmsd":
        assert "declared skip_digestion parameter" in inspect.getdoc(bound)


@pytest.mark.parametrize("heavy_mode", ["off", "force"])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_rmsd_matches_independent_reference_and_preserves_scope_and_units(
    view, heavy_mode, unit
):
    reference = msm.copy(view.molsys)
    args = dict(
        selection=ATOMS,
        structure_indices=SCOPE,
        reference_molecular_system=reference,
        reference_selection=ATOMS[::-1],
        reference_structure_index=1,
        heavy_mode=heavy_mode,
        use_gpu=False,
    )
    xyz = puw.get_value(
        msm.get(
            view.molsys,
            element="atom",
            selection=ATOMS,
            structure_indices=SCOPE,
            coordinates=True,
        ),
        to_unit="nm",
    )
    ref = puw.get_value(
        msm.get(
            reference,
            element="atom",
            selection=ATOMS[::-1],
            structure_indices=[1],
            coordinates=True,
        ),
        to_unit="nm",
    )
    expected = np.sqrt(np.mean(np.sum((xyz - ref) ** 2, axis=-1), axis=1))
    with puw.context(standard_units=[unit, "ps", "radians"]):
        actual = view.addons.molsysmt.structure.get_rmsd(**args, skip_digestion=True)
        assert_native(actual, msm.structure.get_rmsd(view.molsys, **args))
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="nm"), expected, atol=1e-12
    )


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_minimum_rmsd_matches_numpy_kabsch_without_fitting_inputs(view, unit):
    xyz = puw.get_value(
        msm.get(
            view.molsys,
            element="atom",
            selection=ATOMS,
            structure_indices=SCOPE,
            coordinates=True,
        ),
        to_unit="nm",
    )
    ref = puw.get_value(
        msm.get(
            view.molsys,
            element="atom",
            selection=ATOMS,
            structure_indices=[1],
            coordinates=True,
        ),
        to_unit="nm",
    )[0]
    centered_ref = ref - ref.mean(axis=0)
    expected = []
    for frame in xyz:
        centered = frame - frame.mean(axis=0)
        u, _, vt = np.linalg.svd(centered.T @ centered_ref)
        rotation = u @ np.diag([1.0, 1.0, np.linalg.det(u @ vt)]) @ vt
        expected.append(
            np.sqrt(np.mean(np.sum((centered @ rotation - centered_ref) ** 2, axis=1)))
        )
    args = dict(
        selection=ATOMS,
        structure_indices=SCOPE,
        reference_structure_index=1,
        use_gpu=False,
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        actual = view.addons.molsysmt.structure.get_least_rmsd(**args)
        assert_native(actual, msm.structure.get_least_rmsd(view.molsys, **args))
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="nm"), expected, atol=1e-10
    )


def test_translation_changes_raw_rmsd_but_not_minimum_rmsd_or_reference(view):
    reference = msm.copy(view.molsys)
    xyz = msm.get(reference, element="atom", coordinates=True)
    msm.set(reference, coordinates=xyz + puw.quantity([0.2, -0.3, 0.1], "nm"))
    before = puw.get_value(msm.get(reference, element="atom", coordinates=True)).copy()
    args = dict(
        structure_indices=[0],
        reference_molecular_system=reference,
        reference_structure_index=0,
        use_gpu=False,
    )
    raw = view.addons.molsysmt.structure.get_rmsd(**args)
    minimum = view.addons.molsysmt.structure.get_least_rmsd(**args)
    np.testing.assert_allclose(
        puw.get_value(raw, to_unit="nm"), [np.sqrt(0.14)], atol=1e-12
    )
    np.testing.assert_allclose(puw.get_value(minimum, to_unit="nm"), 0, atol=1e-7)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(reference, element="atom", coordinates=True)), before
    )


@pytest.mark.parametrize("kind", ["geometric", "inertia"])
@pytest.mark.parametrize("weights", [None, "masses", [1.0, 2.0, 1.0, 3.0, 2.0]])
def test_principal_axes_native_arrays_orthonormality_and_geometric_oracle(
    view, kind, weights
):
    args = dict(
        selection=ATOMS,
        structure_indices=SCOPE,
        weights=weights,
        principal_axes_type=kind,
        use_gpu=False,
    )
    actual = view.addons.molsysmt.structure.get_principal_axes(**args)
    assert_native(actual, msm.structure.get_principal_axes(view.molsys, **args))
    axes, moments = actual
    assert isinstance(axes, np.ndarray) and isinstance(moments, np.ndarray)
    assert axes.shape == (3, 3, 3) and moments.shape == (3, 3)
    np.testing.assert_allclose(
        axes @ axes.transpose(0, 2, 1),
        np.broadcast_to(np.eye(3), (3, 3, 3)),
        atol=1e-12,
    )
    np.testing.assert_allclose(np.linalg.det(axes), 1, atol=1e-12)
    if kind == "geometric" and isinstance(weights, list):
        xyz = puw.get_value(
            msm.get(
                view.molsys,
                element="atom",
                selection=ATOMS,
                structure_indices=SCOPE,
                coordinates=True,
            ),
            to_unit="nm",
        )
        center = np.average(xyz, weights=weights, axis=1)
        for i, frame in enumerate(xyz - center[:, None]):
            covariance = (frame.T * weights) @ frame / sum(weights)
            values, _ = np.linalg.eigh(covariance)
            np.testing.assert_allclose(moments[i], values, atol=1e-12)
            np.testing.assert_allclose(
                axes[i] @ covariance @ axes[i].T, np.diag(values), atol=1e-12
            )


@pytest.mark.parametrize("heavy_mode", ["off", "force"])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_planes_preserve_memberships_units_and_independent_svd_geometry(
    view, heavy_mode, unit
):
    groups = [[40, 0, 25, 10, 40], [4, 14, 27, 45]]
    args = dict(
        selection=groups, structure_indices=SCOPE, pbc=False, heavy_mode=heavy_mode
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        actual = view.addons.molsysmt.structure.get_least_squares_plane(**args)
        assert_native(
            actual, msm.structure.get_least_squares_plane(view.molsys, **args)
        )
        assert puw.get_unit(actual["centers"]) == puw.unit(unit)
    np.testing.assert_array_equal(actual["structure_indices"], SCOPE)
    for group, (start, stop) in enumerate(
        zip(actual["atom_offsets"][:-1], actual["atom_offsets"][1:])
    ):
        atoms = actual["atom_indices"][start:stop]
        xyz = puw.get_value(
            msm.get(
                view.molsys,
                element="atom",
                selection=atoms,
                structure_indices=SCOPE,
                coordinates=True,
            ),
            to_unit="nm",
        )
        centers = xyz.mean(axis=1)
        np.testing.assert_allclose(
            puw.get_value(actual["centers"], to_unit="nm")[:, group],
            centers,
            atol=1e-12,
        )
        for i, frame in enumerate(xyz - centers[:, None]):
            _, _, vt = np.linalg.svd(frame)
            normal = actual["normals"][i, group]
            assert abs(np.dot(normal, vt[-1])) == pytest.approx(1.0, abs=1e-12)
            residual = frame @ normal
            assert puw.get_value(actual["rms_deviation"], to_unit="nm")[
                i, group
            ] == pytest.approx(np.sqrt(np.mean(residual**2)), abs=1e-12)
            assert puw.get_value(actual["max_deviation"], to_unit="nm")[
                i, group
            ] == pytest.approx(np.max(np.abs(residual)), abs=1e-12)


def test_plane_empty_structure_scope_remains_typed_without_scene_objects(view):
    before = view.export_state()
    actual = view.addons.molsysmt.structure.get_least_squares_plane(
        selection=ATOMS, structure_indices=[]
    )
    expected = msm.structure.get_least_squares_plane(
        view.molsys, selection=ATOMS, structure_indices=[]
    )
    assert_native(actual, expected)
    assert actual["normals"].shape == (0, 1, 3)
    assert actual["structure_indices"].dtype == np.int64
    assert view.export_state() == before


@pytest.mark.parametrize(
    "name,args",
    [
        ("get_rmsd", dict(selection=[0, 1], reference_selection=[0])),
        ("get_least_rmsd", dict(selection=[0, 1], reference_selection=[0])),
        ("get_principal_axes", dict(selection=[])),
        (
            "get_principal_axes",
            dict(selection=ATOMS, weights=[1.0, -1.0, 1.0, 1.0, 1.0]),
        ),
        ("get_least_squares_plane", dict(selection=[0, 1])),
    ],
)
def test_native_rejections_preserve_scene_and_sync_status(view, name, args):
    state = view.export_state()
    status = view.addons.molsysmt.get_sync_status()
    with pytest.raises(Exception) as expected:
        getattr(msm.structure, name)(view.molsys, **args)
    with pytest.raises(type(expected.value)):
        getattr(view.addons.molsysmt.structure, name)(**args)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize("name", NAMES)
def test_readers_preserve_coordinates_box_analysis_and_scene(view, name):
    original = [
        puw.get_value(x).copy()
        for x in msm.get(view.molsys, element="atom", coordinates=True, box=True)
    ]
    analysis = view.molsys.interactions["preserve"]
    state = view.export_state()
    args = dict(structure_indices=SCOPE)
    if name != "get_least_squares_plane":
        args["use_gpu"] = False
    result = getattr(view.addons.molsysmt.structure, name)(**args)
    assert result is not None
    assert view.export_state() == state
    assert view.molsys.interactions["preserve"] is analysis
    for actual, expected in zip(
        msm.get(view.molsys, element="atom", coordinates=True, box=True), original
    ):
        np.testing.assert_array_equal(puw.get_value(actual), expected)


@pytest.mark.parametrize("name", NAMES)
def test_empty_closed_primary_override_and_skip_boundary(name):
    with msv.MolSysView() as empty:
        bound = getattr(empty.addons.molsysmt.structure, name)
        with pytest.raises(ValueError, match="Load a molecular system"):
            bound()
        with pytest.raises(Exception):
            bound(skip_digestion="yes")
        with pytest.raises(TypeError):
            bound(molecular_system=object(), skip_digestion=True)
    with pytest.raises(RuntimeError, match="closed view"):
        bound(skip_digestion=True)


def test_cached_comparison_reader_uses_pending_system_then_replacement(view):
    rmsd = view.addons.molsysmt.structure.get_rmsd
    reference = msm.copy(view.molsys)
    xyz = msm.get(view.molsys, element="atom", structure_indices=[2], coordinates=True)
    view.addons.molsysmt.basic.set(
        structure_indices=[2],
        coordinates=xyz + puw.quantity(0.2, "nm"),
        update_view=False,
    )
    before = view.addons.molsysmt.get_sync_status()
    args = dict(
        structure_indices=[2], reference_molecular_system=reference, use_gpu=False
    )
    assert_native(rmsd(**args), msm.structure.get_rmsd(view.molsys, **args))
    assert view.addons.molsysmt.get_sync_status() == before
    assert before["state"] == "pending"
    view.addons.molsysmt.sync_view()
    with msv.demo["dialanine"] as other:
        view.load(other.molsys, mode="replace")
    view.addons.manager.disable("molsysmt")
    assert_native(
        rmsd(use_gpu=False), msm.structure.get_rmsd(view.molsys, use_gpu=False)
    )
