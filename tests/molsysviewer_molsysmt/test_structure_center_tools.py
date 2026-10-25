"""Receive explicit native centering without adding geometric calculations."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from molsysviewer.system_edits import SystemEditPendingError, SystemEditSyncError
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm

puw = msm.pyunitwizard
SCOPE = [2, 0, 2]


def xyz(molsys):
    return puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm")


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


def test_current_native_signature_defaults_help_and_module_path(view):
    method = view.addons.molsysmt.structure.center
    native = inspect.signature(msm.structure.center).parameters
    bound = inspect.signature(method).parameters
    assert [p for n, p in bound.items() if n != "update_view"] == list(native.values())[
        1:
    ]
    assert bound["update_view"].kind is inspect.Parameter.KEYWORD_ONLY
    assert bound["update_view"].default is True
    assert bound["in_place"].default is False
    assert bound["source_center_selection"].default is None
    assert bound["target_center_selection"].default is None
    assert bound["target_coordinates"].default is None
    assert method.digestion_plan is not None
    assert "center" in dir(view.addons.molsysmt.structure)
    assert not hasattr(view.addons.molsysmt, "center")
    doc = inspect.getdoc(method)
    assert "native in_place=False default" in doc
    assert "No molecular edit" not in doc
    assert "contained" in doc and "snapshot" in doc
    assert "no center calculation" in doc


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "destination", ["origin", "point", "per_structure", "disjoint", "overlap", "inside"]
)
def test_weighted_source_targets_units_repeated_axes_and_native_ownership(
    view, unit, in_place, destination
):
    before, state, target = xyz(view.molsys).copy(), view.export_state(), view.molsys
    moving, source = [6, 2, 0, 2, 4], [2, 0, 2]
    weights = np.array([1.0, 3.0, 4.0])
    weights_before = weights.copy()
    argument = {}
    if destination == "origin":
        targets = np.zeros((len(SCOPE), 3))
    elif destination == "point":
        targets = np.tile([0.1, -0.2, 0.3], (len(SCOPE), 1))
        argument["target_coordinates"] = puw.quantity([1.0, -2.0, 3.0], "angstrom")
    elif destination == "per_structure":
        targets = np.array([[0.1 + 0.02 * s, -0.2, 0.3] for s in SCOPE])
        argument["target_coordinates"] = puw.quantity(targets[:, None, :] * 1000, "pm")
    else:
        atoms = {"disjoint": [1, 3], "overlap": [1, 2], "inside": [0, 2]}[destination]
        targets = before[SCOPE][:, atoms].mean(axis=1)
        argument["target_center_selection"] = atoms
    point_before = (
        None
        if "target_coordinates" not in argument
        else puw.get_value(argument["target_coordinates"]).copy()
    )
    origins = np.average(before[SCOPE][:, source], axis=1, weights=weights)
    expected = before.copy()
    for row, s in enumerate(SCOPE):
        expected[s, np.unique(moving)] = (
            before[s, np.unique(moving)] + targets[row] - origins[row]
        )
    original_analysis = target.interactions["science"]
    box = puw.get_value(msm.get(target, box=True), to_unit="nm").copy()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = view.addons.molsysmt.structure.center(
            selection=moving,
            source_center_selection=source,
            weights=weights,
            structure_indices=SCOPE,
            in_place=in_place,
            **argument,
        )
    output = target if in_place else result
    assert result is None if in_place else result is not target
    assert view.molsys is target
    np.testing.assert_allclose(xyz(output), expected, rtol=0, atol=1e-12)
    np.testing.assert_allclose(
        np.average(xyz(output)[SCOPE][:, source], axis=1, weights=weights),
        targets,
        rtol=0,
        atol=1e-12,
    )
    np.testing.assert_array_equal(weights, weights_before)
    if point_before is not None:
        np.testing.assert_array_equal(
            puw.get_value(argument["target_coordinates"]), point_before
        )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(output, box=True), to_unit="nm"), box
    )
    np.testing.assert_array_equal(
        original_analysis.evaluated_structure_indices, [0, 1, 2]
    )
    np.testing.assert_array_equal(
        output.interactions["science"].evaluated_structure_indices, [1]
    )
    unique = np.unique(moving)
    for s in [0, 2]:
        np.testing.assert_allclose(
            xyz(output)[s, unique][:, None, :] - xyz(output)[s, unique][None, :, :],
            before[s, unique][:, None, :] - before[s, unique][None, :, :],
            rtol=0,
            atol=1e-12,
        )
    if not in_place:
        np.testing.assert_array_equal(xyz(target), before)
        assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("weights", [None, "masses"])
@pytest.mark.parametrize("in_place", [False, True])
def test_default_source_is_moving_population_including_repeated_indices(
    view, weights, in_place
):
    before = xyz(view.molsys).copy()
    moving = [4, 0, 2, 0]
    numerical = (
        None
        if weights is None
        else puw.get_value(
            msm.physchem.get_mass(view.molsys, element="atom", selection=moving)
        )
    )
    origins = np.average(before[:, moving], axis=1, weights=numerical)
    expected = before.copy()
    expected[:, np.unique(moving)] -= origins[:, None, :]
    result = view.addons.molsysmt.structure.center(
        selection=moving, weights=weights, in_place=in_place
    )
    np.testing.assert_allclose(
        xyz(view.molsys if in_place else result), expected, rtol=0, atol=1e-12
    )
    if not in_place:
        np.testing.assert_array_equal(xyz(view.molsys), before)
    else:
        assert result is None


def test_independent_default_is_not_adopted_even_with_deferred_projection_flag(view):
    before, state, target = xyz(view.molsys).copy(), view.export_state(), view.molsys
    result = view.addons.molsysmt.structure.center(update_view=False)
    expected = before - before.mean(axis=1)[:, None, :]
    np.testing.assert_allclose(xyz(result), expected, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(xyz(target), before)
    assert result is not target and view.molsys is target
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


def test_overlapping_target_is_an_initial_snapshot_not_a_final_constraint(view):
    before = xyz(view.molsys).copy()
    initial = before[:, [1, 2]].mean(axis=1)
    result = view.addons.molsysmt.structure.center(
        selection=[0, 2, 4],
        source_center_selection=[0, 2],
        target_center_selection=[1, 2],
    )
    after = xyz(result)
    np.testing.assert_allclose(
        after[:, [0, 2]].mean(axis=1), initial, rtol=0, atol=1e-12
    )
    assert np.max(np.abs(after[:, [1, 2]].mean(axis=1) - initial)) > 1e-8
    np.testing.assert_array_equal(xyz(view.molsys), before)


@pytest.mark.parametrize(
    "arguments",
    [
        {"selection": [0, 2], "source_center_selection": [0, 2, 4]},
        {"selection": [0, 2], "source_center_selection": [1, 3]},
        {"target_center_selection": [0, 1], "target_coordinates": "[1,2,3] nm"},
        {"source_center_selection": []},
        {"target_center_selection": []},
        {"selection": []},
        {"target_coordinates": "[1,2,3] ps"},
        {"target_coordinates": puw.quantity([np.nan, 0, 0], "nm")},
        {"source_center_selection": [0, 2], "weights": [-1.0, 2.0]},
        {"source_center_selection": [0, 2], "weights": [0.0, 0.0]},
        {"structure_indices": []},
        {"structure_indices": [-1]},
        {
            "structure_indices": [2, 0, 2],
            "target_coordinates": puw.quantity(
                [[[0, 0, 0]], [[0, 0, 0]], [[1, 0, 0]]], "nm"
            ),
        },
        {"selection": [99999]},
        {"engine": "unknown"},
    ],
)
def test_native_rejections_do_not_publish_science_or_quarantine_clean_scene(
    view, arguments
):
    native = msm.copy(view.molsys)
    before, state, analysis = (
        xyz(view.molsys).copy(),
        view.export_state(),
        view.molsys.interactions["science"],
    )
    with pytest.raises(Exception) as error:
        msm.structure.center(native, in_place=True, **arguments)
    with pytest.raises(type(error.value)):
        view.addons.molsysmt.structure.center(in_place=True, **arguments)
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.export_state() == state
    assert view.molsys.interactions["science"] is analysis
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("name", ["center_of_selection", "center_coordinates"])
@pytest.mark.parametrize("skip", [False, True])
def test_retired_native_keyword_names_have_no_addon_alias(view, name, skip):
    before, state = xyz(view.molsys).copy(), view.export_state()
    with pytest.raises(Exception) as error:
        msm.structure.center(msm.copy(view.molsys), **{name: None}, skip_digestion=skip)
    with pytest.raises(type(error.value)):
        view.addons.molsysmt.structure.center(**{name: None}, skip_digestion=skip)
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.export_state() == state


@pytest.mark.parametrize("controls", [{"in_place": "yes"}, {"update_view": 1}])
def test_center_integration_flags_remain_guarded_when_digestion_is_skipped(
    view, controls
):
    before, state = xyz(view.molsys).copy(), view.export_state()
    with pytest.raises(Exception):
        view.addons.molsysmt.structure.center(skip_digestion=True, **controls)
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.export_state() == state


def test_deferred_center_removal_and_translation_compose_and_retain_scene(view):
    tools = view.addons.molsysmt
    before = xyz(view.molsys).copy()
    region = view.regions.add(selection=[2, 4], tag="kept")
    saved = view.selections.add("saved", atom_indices=[2, 4])
    sphere = view.shapes.add_sphere(atom_indices=[4], tag="anchor")
    view.active_selection.set([2, 4])
    view.player.go_to_structure(2)
    source = dict(view.load_blocks[0])
    targets = before[[2, 0]][:, [1, 3]].mean(axis=1)
    origins = before[[2, 0]][:, [0, 2]].mean(axis=1)
    expected = before.copy()
    for row, s in enumerate([2, 0]):
        expected[s, [0, 2, 4]] += targets[row] - origins[row]
    tools.structure.center(
        selection=[0, 2, 4],
        source_center_selection=[0, 2],
        target_center_selection=[1, 3],
        structure_indices=[2, 0],
        in_place=True,
        update_view=False,
    )
    assert tools.get_sync_status()["state"] == "pending"
    with pytest.raises(SystemEditPendingError):
        region.hide(skip_digestion=True)
    # Independent results read current pending science, without projection/adoption.
    copy = tools.structure.center()
    np.testing.assert_allclose(
        xyz(copy), expected - expected.mean(axis=1)[:, None, :], rtol=0, atol=1e-12
    )
    assert tools.get_sync_status()["pending_operations"] == 1
    tools.remove(selection=[1], in_place=True, update_view=False)
    expected = np.delete(expected, 1, axis=1)
    tools.structure.translate(
        translation="[0,0,1] nm", in_place=True, update_view=False
    )
    expected[:, :] += [0, 0, 1]
    storage = view.molsys.structures._coordinates
    tools.sync_view()
    np.testing.assert_allclose(xyz(view.molsys), expected, rtol=0, atol=1e-12)
    assert view.molsys.structures._coordinates is storage
    assert view.regions["kept"] is region and region.atom_indices == (1, 3)
    assert view.selections["saved"] is saved and saved.atom_indices == [1, 3]
    assert view.shapes["anchor"] is sphere
    assert view.active_selection.atom_indices == [1, 3] and view.player.index == 2
    assert view.load_blocks[0]["source_id"] == source["source_id"]
    assert tools.get_sync_status()["target_revision"] == 3
    assert not view.history.can_undo()


def test_cached_center_rebinds_and_respects_view_lifetime(view):
    method = view.addons.molsysmt.structure.center
    with msv.demo["dialanine"] as other:
        state = other.export_state()
        view.load(other.molsys, mode="replace")
        before = xyz(view.molsys).copy()
        method(in_place=True)
        np.testing.assert_allclose(
            xyz(view.molsys),
            before - before.mean(axis=1)[:, None, :],
            rtol=0,
            atol=1e-12,
        )
        assert other.export_state() == state
    with pytest.raises(TypeError):
        method(molecular_system=object(), skip_digestion=True)
    view.close()
    with pytest.raises(RuntimeError, match="closed"):
        method(in_place=True)
    with msv.MolSysView() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.structure.center()


class InterruptedCenterWidget(MolSysViewerWidget):
    interrupted = False

    def send(self, content, buffers=None):
        if self.interrupted and content.get("op") == "add_sphere":
            self.interrupted = False
            raise OSError("centering receiving transport interruption")
        return super().send(content, buffers=buffers)


def test_scene_retry_does_not_repeat_native_center_publication():
    with msv.demo["pentalanine"] as source:
        with msv.MolSysView(transport=InterruptedCenterWidget()) as view:
            view.load(source.molsys, structure_indices=[0, 8, 3])
            view.shapes.add_sphere(atom_indices=[0], tag="anchor")
            before = xyz(view.molsys).copy()
            expected = before - before.mean(axis=1)[:, None, :] + [0.1, 0.2, 0.3]
            view._ready = True
            view.widget.interrupted = True
            with pytest.raises(SystemEditSyncError) as error:
                view.addons.molsysmt.structure.center(
                    target_coordinates="[.1,.2,.3] nm", in_place=True
                )
            assert (
                error.value.science_completed is True
                and error.value.scientific_result is None
            )
            assert isinstance(error.value.__cause__, OSError)
            assert view.addons.molsysmt.get_sync_status()["state"] == "sync_failed"
            np.testing.assert_allclose(xyz(view.molsys), expected, rtol=0, atol=1e-12)
            storage = view.molsys.structures._coordinates
            view.addons.molsysmt.sync_view()
            np.testing.assert_allclose(xyz(view.molsys), expected, rtol=0, atol=1e-12)
            assert view.molsys.structures._coordinates is storage
            assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1


def test_interrupted_center_pipeline_requires_explicit_recovery(view):
    from molsysviewer_molsysmt._geometry import (
        _geometry_token,
        _prepare_geometry_transform,
    )

    before = xyz(view.molsys).copy()

    def prepare(target):
        plan = _prepare_geometry_transform(
            target,
            "center",
            dict(
                selection="all",
                structure_indices="all",
                syntax="MolSysMT",
                in_place=True,
                target_coordinates="[1,2,3] nm",
            ),
        )
        native_run = plan["run"]

        def interrupted_pipeline():
            native_run()
            raise RuntimeError("interruption after native centering publication")

        plan["run"] = interrupted_pipeline
        return plan

    with pytest.raises(RuntimeError, match="after native centering publication"):
        view.addons.manager.system_edits.execute(
            prepare, name="receiving.center", rejection_check=_geometry_token
        )
    expected = before - before.mean(axis=1)[:, None, :] + [1, 2, 3]
    np.testing.assert_allclose(xyz(view.molsys), expected, rtol=0, atol=1e-12)
    assert view.addons.molsysmt.get_sync_status()["state"] == "uncertain"
    with pytest.raises(SystemEditPendingError):
        view.addons.molsysmt.sync_view()
