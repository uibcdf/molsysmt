"""Receive proper principal-axis rotations with independent tensor invariants."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from molsysviewer.system_edits import SystemEditPendingError, SystemEditSyncError
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm

puw = msm.pyunitwizard
FIT = [0, 1, 2, 3, 4, 5]
MOVING = list(range(8))
SCOPE = [2, 0, 2]
TARGET = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]])


def xyz(molsys):
    return puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm")


def covariance(points, weights):
    center = np.average(points, axis=0, weights=weights)
    delta = points - center
    return center, (delta * weights[:, None]).T @ delta / weights.sum()


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            msm.set(
                result.molsys, box=puw.quantity(np.tile(np.eye(3) * 3, (3, 1, 1)), "nm")
            )
            analysis = msm.interactions.hbonds.get_buch_hbonds(
                result.molsys,
                structure_indices="all",
                pbc=False,
                output_type="molsysmt.Interactions",
            )
            result.interactions.attach(analysis, name="science", assume_aligned=True)
            result.interactions.add("science", tag="hb")
            yield result


def test_signature_defaults_expert_path_and_addon_only_digestion(view):
    method = view.addons.molsysmt.structure.align_principal_axes
    native = inspect.signature(msm.structure.align_principal_axes).parameters
    bound = inspect.signature(method).parameters
    assert [
        p for n, p in bound.items() if n not in {"skip_digestion", "update_view"}
    ] == list(native.values())[1:]
    assert "skip_digestion" not in native
    for name, default in [("skip_digestion", False), ("update_view", True)]:
        assert bound[name].kind is inspect.Parameter.KEYWORD_ONLY
        assert bound[name].default is default
    assert bound["in_place"].default is False
    assert bound["center"].default is False
    assert bound["principal_axes_of_selection"].default is None
    assert method.digestion_plan is not None
    assert "align_principal_axes" in dir(view.addons.molsysmt.structure)
    assert not hasattr(view.addons.molsysmt, "align_principal_axes")
    doc = inspect.getdoc(method)
    assert "native in_place=False default" in doc
    assert "No molecular edit" not in doc
    assert "always receives ordinary validation" in doc
    assert "right-handed" in doc and "no eigensolver" in doc


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("kind", ["inertia", "geometric"])
@pytest.mark.parametrize("centered", [False, True])
@pytest.mark.parametrize("custom_basis", [False, True])
@pytest.mark.parametrize("in_place", [False, True])
def test_weighted_tensor_alignment_units_repeated_structures_and_native_ownership(
    view, unit, kind, centered, custom_basis, in_place
):
    target, state = view.molsys, view.export_state()
    before = xyz(target).copy()
    weights = np.array([1.0, 3.0, 2.0, 4.0, 5.0, 2.0])
    basis = TARGET.copy() if custom_basis else np.eye(3)
    arguments = dict(
        selection=MOVING,
        principal_axes_of_selection=FIT,
        principal_axes_type=kind,
        structure_indices=SCOPE,
        weights=weights,
        center=centered,
        in_place=in_place,
    )
    if custom_basis:
        arguments["axes"] = basis
    original_analysis = target.interactions["science"]
    box = puw.get_value(msm.get(target, box=True), to_unit="nm").copy()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = view.addons.molsysmt.structure.align_principal_axes(**arguments)
    output = target if in_place else result
    assert result is None if in_place else result is not target
    assert view.molsys is target
    after = xyz(output)
    assert after.shape == before.shape
    for s in [0, 2]:
        initial_center, initial_cov = covariance(before[s, FIT], weights)
        final_center, final_cov = covariance(after[s, FIT], weights)
        values = np.linalg.eigvalsh(initial_cov)
        if kind == "inertia":
            values = values[::-1]
        np.testing.assert_allclose(
            basis @ final_cov @ basis.T, np.diag(values), rtol=0, atol=1e-12
        )
        np.testing.assert_allclose(
            final_center,
            np.zeros(3) if centered else initial_center,
            rtol=0,
            atol=1e-12,
        )
        # Rigid proper rotation: distances and signed tetrahedral volume survive.
        for coordinates in [before, after]:
            assert np.isfinite(coordinates).all()
        initial_vectors = before[s, MOVING][:, None] - before[s, MOVING][None, :]
        final_vectors = after[s, MOVING][:, None] - after[s, MOVING][None, :]
        np.testing.assert_allclose(
            np.linalg.norm(final_vectors, axis=-1),
            np.linalg.norm(initial_vectors, axis=-1),
            rtol=0,
            atol=1e-12,
        )
        np.testing.assert_allclose(
            np.linalg.det(after[s, [1, 2, 3]] - after[s, 0]),
            np.linalg.det(before[s, [1, 2, 3]] - before[s, 0]),
            rtol=0,
            atol=1e-12,
        )
        assert np.max(np.abs(after[s, MOVING] - before[s, MOVING])) > 1e-5
        np.testing.assert_array_equal(after[s, 8:], before[s, 8:])
    np.testing.assert_array_equal(after[1], before[1])
    np.testing.assert_array_equal(weights, [1.0, 3.0, 2.0, 4.0, 5.0, 2.0])
    if custom_basis:
        np.testing.assert_array_equal(basis, TARGET)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(output, box=True), to_unit="nm"), box
    )
    np.testing.assert_array_equal(
        original_analysis.evaluated_structure_indices, [0, 1, 2]
    )
    np.testing.assert_array_equal(
        output.interactions["science"].evaluated_structure_indices, [1]
    )
    if not in_place:
        np.testing.assert_array_equal(xyz(target), before)
        assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("weights", [None, "masses"])
@pytest.mark.parametrize("kind", ["inertia", "geometric"])
def test_default_fit_population_and_mass_weights(view, weights, kind):
    before = xyz(view.molsys).copy()
    numerical = (
        np.ones(len(MOVING))
        if weights is None
        else puw.get_value(
            msm.physchem.get_mass(view.molsys, element="atom", selection=MOVING)
        )
    )
    result = view.addons.molsysmt.structure.align_principal_axes(
        selection=MOVING,
        principal_axes_type=kind,
        weights=weights,
        center=True,
    )
    for s in range(3):
        _, expected = covariance(before[s, MOVING], numerical)
        center, observed = covariance(xyz(result)[s, MOVING], numerical)
        values = np.linalg.eigvalsh(expected)
        if kind == "inertia":
            values = values[::-1]
        np.testing.assert_allclose(center, 0, atol=1e-12)
        np.testing.assert_allclose(observed, np.diag(values), atol=1e-12)
    np.testing.assert_array_equal(xyz(view.molsys), before)


def test_all_native_defaults_keep_independent_output_and_initial_center(view):
    before, state = xyz(view.molsys).copy(), view.export_state()
    result = view.addons.molsysmt.structure.align_principal_axes(update_view=False)
    for s in range(3):
        center, original = covariance(before[s], np.ones(before.shape[1]))
        observed_center, observed = covariance(xyz(result)[s], np.ones(before.shape[1]))
        np.testing.assert_allclose(observed_center, center, atol=1e-12)
        np.testing.assert_allclose(
            observed, np.diag(np.linalg.eigvalsh(original)[::-1]), atol=1e-12
        )
    assert view.export_state() == state
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


@pytest.mark.parametrize(
    "arguments",
    [
        {"axes": [[1, 0, 0], [0, 1, 0], [0, 0, -1]]},
        {"axes": [[2, 0, 0], [0, 1, 0], [0, 0, 1]]},
        {"axes": np.full((3, 3), np.nan)},
        {"axes": [1, 0, 0]},
        {"principal_axes_of_selection": []},
        {"weights": [1.0, -1.0, 1.0, 1.0, 1.0, 1.0]},
        {"structure_indices": []},
        {"structure_indices": [-1]},
        {"selection": [99999]},
        {"engine": "unknown"},
        {"center": 1},
    ],
)
def test_native_rejections_preserve_geometry_coverage_and_clean_scene(view, arguments):
    params = dict(selection=MOVING, principal_axes_of_selection=FIT, in_place=True)
    params.update(arguments)
    before, state = xyz(view.molsys).copy(), view.export_state()
    analysis = view.molsys.interactions["science"]
    with pytest.raises(Exception) as native:
        msm.structure.align_principal_axes(msm.copy(view.molsys), **params)
    with pytest.raises(type(native.value)):
        view.addons.molsysmt.structure.align_principal_axes(**params)
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.molsys.interactions["science"] is analysis
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("kind", ["inertia", "geometric"])
def test_degenerate_principal_moments_reject_before_any_publication(view, kind):
    points = np.vstack([np.eye(3), -np.eye(3)])
    coordinates = xyz(view.molsys).copy()
    coordinates[:, FIT] = points
    view.addons.molsysmt.basic.set(coordinates=puw.quantity(coordinates, "nm"))
    state = view.export_state()
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    with pytest.raises(Exception) as native:
        msm.structure.align_principal_axes(
            msm.copy(view.molsys),
            selection=FIT,
            principal_axes_type=kind,
            in_place=True,
        )
    with pytest.raises(type(native.value)):
        view.addons.molsysmt.structure.align_principal_axes(
            selection=FIT, principal_axes_type=kind, in_place=True
        )
    np.testing.assert_array_equal(xyz(view.molsys), coordinates)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize(
    "flags", [{"in_place": "yes"}, {"update_view": 1}, {"center": 1}]
)
def test_addon_skip_cannot_bypass_integration_or_native_validation(view, flags):
    before = xyz(view.molsys).copy()
    with pytest.raises(Exception):
        view.addons.molsysmt.structure.align_principal_axes(
            skip_digestion=True, **flags
        )
    np.testing.assert_array_equal(xyz(view.molsys), before)


def test_deferred_rotation_removal_and_translation_preserve_scene_correspondence(view):
    tools = view.addons.molsysmt
    region = view.regions.add(selection=[2, 4], tag="kept")
    saved = view.selections.add("saved", atom_indices=[2, 4])
    sphere = view.shapes.add_sphere(atom_indices=[4], tag="anchor")
    view.active_selection.set([2, 4])
    view.player.go_to_structure(2)
    source_id = view.load_blocks[0]["source_id"]
    tools.structure.align_principal_axes(
        selection=MOVING,
        principal_axes_of_selection=FIT,
        structure_indices=[2, 0],
        center=True,
        in_place=True,
        update_view=False,
    )
    expected = xyz(view.molsys).copy()
    assert tools.get_sync_status()["state"] == "pending"
    with pytest.raises(SystemEditPendingError):
        region.hide(skip_digestion=True)
    tools.basic.remove(selection=[1], in_place=True, update_view=False)
    expected = np.delete(expected, 1, axis=1)
    tools.structure.translate(
        translation="[0, 0, 1] nm", in_place=True, update_view=False
    )
    expected += [0, 0, 1]
    storage = view.molsys.structures._coordinates
    tools.sync_view()
    np.testing.assert_allclose(xyz(view.molsys), expected, rtol=0, atol=1e-12)
    assert view.molsys.structures._coordinates is storage
    assert view.regions["kept"] is region and region.atom_indices == (1, 3)
    assert view.selections["saved"] is saved and saved.atom_indices == [1, 3]
    assert view.shapes["anchor"] is sphere
    assert view.active_selection.atom_indices == [1, 3] and view.player.index == 2
    assert view.load_blocks[0]["source_id"] == source_id
    assert tools.get_sync_status()["target_revision"] == 3
    assert not view.history.can_undo()


def test_cached_callable_rebinds_to_current_system_and_respects_lifetime(view):
    method = view.addons.molsysmt.structure.align_principal_axes
    with msv.demo["dialanine"] as other:
        before_other, state = xyz(other.molsys).copy(), other.export_state()
        view.load(other.molsys, mode="replace")
        method(center=True, in_place=True)
        np.testing.assert_allclose(xyz(view.molsys).mean(axis=1), 0, atol=1e-12)
        np.testing.assert_array_equal(xyz(other.molsys), before_other)
        assert other.export_state() == state
    with pytest.raises(TypeError):
        method(molecular_system=object(), skip_digestion=True)
    view.close()
    with pytest.raises(RuntimeError, match="closed"):
        method()
    with msv.MolSysView() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.structure.align_principal_axes()


class InterruptedAxesWidget(MolSysViewerWidget):
    interrupted = False

    def send(self, content, buffers=None):
        if self.interrupted and content.get("op") == "add_sphere":
            self.interrupted = False
            raise OSError("principal-axis receiving transport interruption")
        return super().send(content, buffers=buffers)


def test_scene_retry_does_not_repeat_native_alignment():
    with msv.demo["pentalanine"] as source:
        with msv.MolSysView(transport=InterruptedAxesWidget()) as view:
            view.load(source.molsys, structure_indices=[0, 8, 3])
            view.shapes.add_sphere(atom_indices=[0], tag="anchor")
            view._ready = True
            view.widget.interrupted = True
            with pytest.raises(SystemEditSyncError) as error:
                view.addons.molsysmt.structure.align_principal_axes(
                    center=True, in_place=True
                )
            assert (
                error.value.science_completed is True
                and error.value.scientific_result is None
            )
            assert isinstance(error.value.__cause__, OSError)
            assert view.addons.molsysmt.get_sync_status()["state"] == "sync_failed"
            expected = xyz(view.molsys).copy()
            storage = view.molsys.structures._coordinates
            view.addons.molsysmt.sync_view()
            assert view.molsys.structures._coordinates is storage
            np.testing.assert_array_equal(xyz(view.molsys), expected)
            assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1


@pytest.mark.parametrize("centered", [False, True])
def test_fitting_population_may_be_disjoint_from_atoms_moved(view, centered):
    before = xyz(view.molsys).copy()
    weights = np.array([1.0, 3.0, 2.0, 4.0, 5.0, 2.0])
    source_center, _ = covariance(before[2, FIT], weights)
    source_axes, _ = msm.structure.get_principal_axes(
        view.molsys,
        selection=FIT,
        structure_indices=[2],
        weights=weights,
    )
    moving = [6, 7, 8, 9]
    expected = before.copy()
    expected[2, moving] = (
        (before[2, moving] - source_center) @ source_axes[0].T @ TARGET
    )
    if not centered:
        expected[2, moving] += source_center
    result = view.addons.molsysmt.structure.align_principal_axes(
        selection=moving,
        principal_axes_of_selection=FIT,
        structure_indices=[2],
        weights=weights,
        axes=TARGET,
        center=centered,
    )
    np.testing.assert_allclose(xyz(result), expected, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(xyz(result)[:, FIT], before[:, FIT])
    np.testing.assert_array_equal(xyz(view.molsys), before)
