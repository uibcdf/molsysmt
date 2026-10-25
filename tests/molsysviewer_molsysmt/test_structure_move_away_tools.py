"""Receive native single-structure displacement and explicit failure ownership."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from molsysviewer.system_edits import SystemEditPendingError, SystemEditSyncError
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm

puw = msm.pyunitwizard


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


def test_signature_defaults_help_and_expert_path(view):
    method = view.addons.molsysmt.structure.move_away
    native, bound = (
        inspect.signature(msm.structure.move_away),
        inspect.signature(method),
    )
    assert [p for n, p in bound.parameters.items() if n != "update_view"] == list(
        native.parameters.values()
    )[1:]
    assert bound.parameters["update_view"].kind is inspect.Parameter.KEYWORD_ONLY
    assert bound.parameters["update_view"].default is True
    assert bound.parameters["in_place"].default is False
    assert bound.parameters["structure_indices"].default == 0
    assert method.digestion_plan is not None
    assert "move_away" in dir(view.addons.molsysmt.structure)
    assert not hasattr(view.addons.molsysmt, "move_away")
    doc = inspect.getdoc(method)
    assert "native in_place=False default" in doc
    assert "No molecular edit" not in doc
    assert "single-structure" in doc and "NaNs" in doc
    assert "no substitute geometry" in doc


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("mode", ["auto", "explicit"])
@pytest.mark.parametrize("external", [False, True])
@pytest.mark.parametrize("in_place", [False, True])
def test_single_structure_weighted_centers_units_reference_and_native_return(
    view, unit, mode, external, in_place
):
    target, state = view.molsys, view.export_state()
    before = xyz(target).copy()
    moving, source, ref_atoms = [0, 2, 4], [0, 2], [1, 3]
    weights, ref_weights = np.array([1.0, 3.0]), np.array([2.0, 1.0])
    arguments = dict(
        selection=moving,
        center_of_selection=source,
        weights=weights,
        reference_center_of_selection=ref_atoms,
        reference_weights=ref_weights,
        structure_indices=[2],
        reference_structure_indices=[1],
        in_place=in_place,
    )
    reference = msm.copy(target) if external else target
    if external:
        msm.structure.translate(reference, translation="[1, -2, .5] nm", in_place=True)
        arguments["reference_molecular_system"] = reference
    ref_before = xyz(reference).copy()
    source_center = np.average(before[2, source], axis=0, weights=weights)
    ref_center = np.average(ref_before[1, ref_atoms], axis=0, weights=ref_weights)
    if mode == "auto":
        delta = source_center - ref_center
        delta = 0.3 * delta / np.linalg.norm(delta)
    else:
        arguments["direction"] = [2, -1, 2]
        delta = ref_center + 0.3 * np.array([2, -1, 2]) / 3 - source_center
    expected = before.copy()
    expected[2, moving] += delta
    original_analysis = target.interactions["science"]
    box = puw.get_value(msm.get(target, box=True), to_unit="nm").copy()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = view.addons.molsysmt.structure.move_away(**arguments)
    output = target if in_place else result
    assert result is None if in_place else result is not target
    assert view.molsys is target
    np.testing.assert_allclose(xyz(output), expected, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(output, box=True), to_unit="nm"), box
    )
    np.testing.assert_array_equal(
        original_analysis.evaluated_structure_indices, [0, 1, 2]
    )
    np.testing.assert_array_equal(
        output.interactions["science"].evaluated_structure_indices, [0, 1]
    )
    np.testing.assert_array_equal(weights, [1.0, 3.0])
    np.testing.assert_array_equal(ref_weights, [2.0, 1.0])
    np.testing.assert_allclose(
        xyz(output)[2, moving][:, None] - xyz(output)[2, moving][None, :],
        before[2, moving][:, None] - before[2, moving][None, :],
        rtol=0,
        atol=1e-12,
    )
    if external:
        np.testing.assert_array_equal(xyz(reference), ref_before)
    if not in_place:
        np.testing.assert_array_equal(xyz(target), before)
        assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("weights", [None, "masses"])
def test_auto_mode_is_incremental_displacement_and_default_scope_is_zero(view, weights):
    before = xyz(view.molsys).copy()
    source, refs = [0, 2], [1, 3]
    numeric = (
        None
        if weights is None
        else puw.get_value(
            msm.physchem.get_mass(view.molsys, element="atom", selection=source)
        )
    )
    center = np.average(before[0, source], axis=0, weights=numeric)
    ref = before[0, refs].mean(axis=0)
    axis = (center - ref) / np.linalg.norm(center - ref)
    result = view.addons.molsysmt.structure.move_away(
        selection=[0, 2, 4],
        center_of_selection=source,
        weights=weights,
        reference_center_of_selection=refs,
        distance="2 angstroms",
        update_view=False,
    )
    expected = before.copy()
    expected[0, [0, 2, 4]] += 0.2 * axis
    np.testing.assert_allclose(xyz(result), expected, rtol=0, atol=1e-12)
    np.testing.assert_allclose(
        np.linalg.norm(
            np.average(xyz(result)[0, source], axis=0, weights=numeric) - ref
        ),
        np.linalg.norm(center - ref) + 0.2,
        atol=1e-12,
    )
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


@pytest.mark.parametrize(
    "arguments",
    [
        {"distance": "1 ps"},
        {"selection": [99999]},
        {"structure_indices": [-1]},
        {"direction": [1, 0]},
        {"selection": [0, 2], "center_of_selection": [1, 3], "direction": [1, 0, 0]},
        {"structure_indices": [2, 0]},
    ],
)
def test_native_rejection_without_writes_keeps_clean_scene(view, arguments):
    params = dict(
        selection=[0, 2, 4],
        center_of_selection=[0, 2],
        reference_center_of_selection=[1, 3],
        in_place=True,
    )
    params.update(arguments)
    before, state = xyz(view.molsys).copy(), view.export_state()
    with pytest.raises(Exception) as native:
        msm.structure.move_away(msm.copy(view.molsys), **params)
    with pytest.raises(type(native.value)):
        view.addons.molsysmt.structure.move_away(**params)
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("flags", [{"in_place": "yes"}, {"update_view": 1}])
def test_integration_flags_remain_guarded_with_skipped_digestion(view, flags):
    before = xyz(view.molsys).copy()
    with pytest.raises(Exception):
        view.addons.molsysmt.structure.move_away(
            direction=[1, 0, 0], skip_digestion=True, **flags
        )
    np.testing.assert_array_equal(xyz(view.molsys), before)


def test_deferred_edit_removal_scene_maps_and_retry_without_science(view):
    tools = view.addons.molsysmt
    before = xyz(view.molsys).copy()
    region = view.regions.add(selection=[2, 4], tag="kept")
    saved = view.selections.add("saved", atom_indices=[2, 4])
    sphere = view.shapes.add_sphere(atom_indices=[4], tag="anchor")
    view.active_selection.set([2, 4])
    view.player.go_to_structure(2)
    source_id = view.load_blocks[0]["source_id"]
    center = before[2, [0, 2]].mean(axis=0)
    ref = before[2, [1, 3]].mean(axis=0)
    expected = before.copy()
    expected[2, [0, 2, 4]] += ref + [0.3, 0, 0] - center
    tools.structure.move_away(
        selection=[0, 2, 4],
        center_of_selection=[0, 2],
        reference_center_of_selection=[1, 3],
        structure_indices=2,
        direction=[1, 0, 0],
        in_place=True,
        update_view=False,
    )
    assert tools.get_sync_status()["state"] == "pending"
    with pytest.raises(SystemEditPendingError):
        region.hide(skip_digestion=True)
    tools.basic.remove(selection=[1], in_place=True, update_view=False)
    expected = np.delete(expected, 1, axis=1)
    storage = view.molsys.structures._coordinates
    tools.sync_view()
    np.testing.assert_allclose(xyz(view.molsys), expected, rtol=0, atol=1e-12)
    assert view.molsys.structures._coordinates is storage
    assert view.regions["kept"] is region and region.atom_indices == (1, 3)
    assert view.selections["saved"] is saved and saved.atom_indices == [1, 3]
    assert view.shapes["anchor"] is sphere
    assert view.active_selection.atom_indices == [1, 3] and view.player.index == 2
    assert view.load_blocks[0]["source_id"] == source_id
    assert tools.get_sync_status()["target_revision"] == 2
    assert not view.history.can_undo()


def test_cached_callable_rebinds_target_and_respects_lifetime(view):
    method = view.addons.molsysmt.structure.move_away
    with msv.demo["dialanine"] as other:
        state = other.export_state()
        view.load(other.molsys, mode="replace")
        before = xyz(view.molsys).copy()
        result = method(direction=[1, 0, 0])
        expected = before.copy()
        expected[0] += [0.3, 0, 0]
        np.testing.assert_allclose(xyz(result), expected, rtol=0, atol=1e-12)
        np.testing.assert_array_equal(xyz(view.molsys), before)
        assert other.export_state() == state
    with pytest.raises(TypeError):
        method(molecular_system=object(), skip_digestion=True)
    view.close()
    with pytest.raises(RuntimeError, match="closed"):
        method(direction=[1, 0, 0])
    with msv.MolSysView() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.structure.move_away(direction=[1, 0, 0])


class InterruptedMoveWidget(MolSysViewerWidget):
    interrupted = False

    def send(self, content, buffers=None):
        if self.interrupted and content.get("op") == "add_sphere":
            self.interrupted = False
            raise OSError("displacement receiving transport interruption")
        return super().send(content, buffers=buffers)


def test_sync_failure_retries_projection_without_repeating_displacement():
    with msv.demo["pentalanine"] as source:
        with msv.MolSysView(transport=InterruptedMoveWidget()) as view:
            view.load(source.molsys, structure_indices=[0, 8, 3])
            view.shapes.add_sphere(atom_indices=[0], tag="anchor")
            before = xyz(view.molsys).copy()
            expected = before.copy()
            expected[0] += [0.3, 0, 0]
            view._ready = True
            view.widget.interrupted = True
            with pytest.raises(SystemEditSyncError) as error:
                view.addons.molsysmt.structure.move_away(
                    direction=[1, 0, 0], in_place=True
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
            assert view.molsys.structures._coordinates is storage
            np.testing.assert_allclose(xyz(view.molsys), expected, rtol=0, atol=1e-12)
            assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1
