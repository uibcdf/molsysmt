"""Receive native translation as independent output and managed geometry edits."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from molsysviewer.system_edits import SystemEditPendingError, SystemEditSyncError
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm

puw = msm.pyunitwizard
READERS = (
    "get_distances",
    "get_vectors",
    "get_center",
    "get_radius_of_gyration",
    "get_angles",
    "get_dihedral_angles",
    "get_rmsd",
    "get_least_rmsd",
    "get_principal_axes",
    "get_least_squares_plane",
    "get_maximum_distances",
    "get_contacts",
    "get_rmsf",
    "get_minimum_distances",
    "get_neighbors",
    "get_symmetry_corrected_rmsd",
    "get_secondary_structure",
    "principal_component_analysis",
)


def values(view):
    return puw.get_value(msm.get(view.molsys, coordinates=True), to_unit="nm")


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


def test_signature_help_namespace_and_explicit_integration_controls(view):
    method = view.addons.molsysmt.structure.translate
    parameters = inspect.signature(method).parameters
    assert [p for name, p in parameters.items() if name != "update_view"] == list(
        inspect.signature(msm.structure.translate).parameters.values()
    )[1:]
    assert parameters["update_view"].kind is inspect.Parameter.KEYWORD_ONLY
    assert parameters["update_view"].default is True
    assert parameters["in_place"].default is False
    assert method.digestion_plan is not None
    assert "native in_place=False default" in inspect.getdoc(method)
    assert "No molecular edit" not in inspect.getdoc(method)
    assert set(dir(view.addons.molsysmt.structure)) == set(READERS + ("translate",))
    assert not hasattr(view.addons.molsysmt, "translate")


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("kind", ["single", "structures", "atoms"])
@pytest.mark.parametrize("in_place", [False, True])
def test_native_displacements_units_repetitions_and_independent_ownership(
    view, unit, kind, in_place
):
    first = values(view).copy()
    selection, frames = [2, 0, 2], [2, 0, 2]
    shape = {"single": (1, 1, 3), "structures": (3, 1, 3), "atoms": (3, 3, 3)}[kind]
    displacement = (np.arange(np.prod(shape)).reshape(shape) + 1) / 100
    translation = puw.convert(puw.quantity(displacement, "nm"), to_unit="angstrom")
    unchanged_translation = puw.get_value(translation).copy()
    expected = first.copy()
    broadcast = np.broadcast_to(displacement, (3, 3, 3))
    # Native repeated axes use last supplied values, never repeated accumulation.
    for si, s in enumerate(frames):
        for ai, a in enumerate(selection):
            expected[s, a] = first[s, a] + broadcast[si, ai]
    target, state = view.molsys, view.export_state()
    original_analysis = target.interactions["science"]
    old_box = puw.get_value(msm.get(target, box=True), to_unit="nm").copy()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = view.addons.molsysmt.structure.translate(
            translation=translation,
            selection=selection,
            structure_indices=frames,
            in_place=in_place,
        )
    output = view.molsys if in_place else result
    assert view.molsys is target
    assert result is None if in_place else output is not target
    np.testing.assert_allclose(
        puw.get_value(msm.get(output, coordinates=True), to_unit="nm"),
        expected,
        atol=1e-12,
    )
    np.testing.assert_array_equal(puw.get_value(translation), unchanged_translation)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(output, box=True), to_unit="nm"), old_box
    )
    np.testing.assert_array_equal(
        original_analysis.evaluated_structure_indices, [0, 1, 2]
    )
    np.testing.assert_array_equal(
        output.interactions["science"].evaluated_structure_indices, [1]
    )
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
    if not in_place:
        np.testing.assert_array_equal(values(view), first)
        assert target.interactions["science"] is original_analysis
        assert view.export_state() == state


def test_default_independent_translation_is_never_adopted_by_update_control(view):
    state, target, before = view.export_state(), view.molsys, values(view).copy()
    result = view.addons.molsysmt.structure.translate(
        translation="[1, 2, 3] angstrom", update_view=False
    )
    assert result is not target and view.molsys is target
    np.testing.assert_allclose(
        puw.get_value(msm.get(result, coordinates=True), to_unit="nm"),
        before + [0.1, 0.2, 0.3],
    )
    np.testing.assert_array_equal(values(view), before)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


def test_immediate_translation_retains_scene_identities_navigation_and_sources(view):
    target = view.molsys
    region = view.regions.add(selection=[0, 2, 4], tag="region")
    saved = view.selections.add("saved", atom_indices=[0, 2])
    view.active_selection.set([0, 2])
    sphere = view.shapes.add_sphere(atom_indices=[2], tag="anchor")
    view.player.go_to_structure(2)
    source = dict(view.load_blocks[0])
    before = values(view).copy()
    result = view.addons.molsysmt.structure.translate(
        translation="[1, 0, 0] angstrom",
        selection=[0, 2],
        structure_indices=[2],
        in_place=True,
    )
    assert result is None and view.molsys is target
    assert view.regions["region"] is region and region.atom_indices == (0, 2, 4)
    assert view.selections["saved"] is saved and saved.atom_indices == [0, 2]
    assert view.shapes["anchor"] is sphere
    assert view.active_selection.atom_indices == [0, 2] and view.player.index == 2
    assert view.load_blocks[0]["source_id"] == source["source_id"]
    expected = before.copy()
    expected[2, [0, 2]] += [0.1, 0, 0]
    np.testing.assert_allclose(values(view), expected)
    assert not view.history.can_undo()
    np.testing.assert_array_equal(
        view.molsys.interactions["science"].evaluated_structure_indices, [0, 1]
    )


def test_deferred_translations_and_removal_compose_without_science_replay(view):
    tools = view.addons.molsysmt
    region = view.regions.add(selection=[2, 4], tag="retained")
    before = values(view).copy()
    tools.structure.translate(
        translation="[1, 0, 0] nm",
        structure_indices=[2],
        in_place=True,
        update_view=False,
    )
    assert tools.get_sync_status()["state"] == "pending"
    assert view._current_molecular_projection is None
    with pytest.raises(SystemEditPendingError):
        region.hide(skip_digestion=True)
    # Independent outputs can read pending science without projecting it.
    independent = tools.structure.translate(translation="[0, 1, 0] nm")
    np.testing.assert_allclose(
        puw.get_value(msm.get(independent, coordinates=True), to_unit="nm"),
        values(view) + [0, 1, 0],
    )
    assert tools.get_sync_status()["pending_operations"] == 1
    tools.remove(selection=[0], in_place=True, update_view=False)
    tools.structure.translate(
        translation="[0, 0, 1] nm",
        selection=[1],
        structure_indices=[0],
        in_place=True,
        update_view=False,
    )
    assert tools.get_sync_status()["pending_operations"] == 3
    expected = before.copy()
    expected[2] += [1, 0, 0]
    expected = expected[:, 1:]
    expected[0, 1] += [0, 0, 1]
    storage = view.molsys.structures._coordinates
    tools.sync_view()
    np.testing.assert_allclose(values(view), expected)
    assert view.molsys.structures._coordinates is storage
    assert view.regions["retained"] is region and region.atom_indices == (1, 3)
    np.testing.assert_array_equal(
        view.molsys.interactions["science"].evaluated_structure_indices, [1]
    )


@pytest.mark.parametrize(
    "arguments",
    [
        {"translation": "1 ps"},
        {"translation": None},
        {"translation": puw.quantity(np.ones((2, 2, 3)), "nm")},
        {"translation": "[1, 0, 0] nm", "selection": [99999]},
        {"translation": "[1, 0, 0] nm", "structure_indices": [99999]},
    ],
)
def test_native_rejections_leave_scene_science_and_sync_state_unchanged(
    view, arguments
):
    native = msm.copy(view.molsys)
    state, before, analysis = (
        view.export_state(),
        values(view).copy(),
        view.molsys.interactions["science"],
    )
    with pytest.raises(Exception) as error:
        msm.structure.translate(native, in_place=True, **arguments)
    with pytest.raises(type(error.value)):
        view.addons.molsysmt.structure.translate(in_place=True, **arguments)
    np.testing.assert_array_equal(values(view), before)
    assert (
        view.molsys.interactions["science"] is analysis and view.export_state() == state
    )
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize(
    "arguments", [{"in_place": "yes"}, {"update_view": "yes"}, {"update_view": 1}]
)
def test_integration_branch_guards_survive_skip_digestion(view, arguments):
    state = view.export_state()
    with pytest.raises(Exception):
        view.addons.molsysmt.structure.translate(
            translation=puw.quantity(np.ones((1, 1, 3)), "nm"),
            skip_digestion=True,
            **arguments,
        )
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


@pytest.mark.parametrize("empty", [{"selection": []}, {"structure_indices": []}])
def test_empty_write_preserves_coverage_and_revision(view, empty):
    before = values(view).copy()
    analysis = view.molsys.interactions["science"]
    assert (
        view.addons.molsysmt.structure.translate(
            translation="[1, 0, 0] nm", in_place=True, **empty
        )
        is None
    )
    np.testing.assert_array_equal(values(view), before)
    assert view.molsys.interactions["science"] is analysis
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


def test_cached_transform_lifetime_and_replacement_are_view_local(view):
    method = view.addons.molsysmt.structure.translate
    with msv.demo["dialanine"] as second:
        other_state = second.export_state()
        view.load(second.molsys, mode="replace")
        before = values(view).copy()
        method(translation="[0, 0, 1] nm", in_place=True)
        np.testing.assert_allclose(values(view), before + [0, 0, 1])
        assert second.export_state() == other_state
    with pytest.raises(TypeError):
        method(molecular_system=object(), skip_digestion=True)
    view.close()
    with pytest.raises(RuntimeError, match="closed"):
        method(translation="[0, 0, 1] nm", in_place=True)
    with msv.MolSysView() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.structure.translate(translation="[0, 0, 1] nm")


class InterruptedWidget(MolSysViewerWidget):
    interrupted = False

    def send(self, content, buffers=None):
        if self.interrupted and content.get("op") == "add_sphere":
            self.interrupted = False
            raise OSError("receiving translation connector interruption")
        return super().send(content, buffers=buffers)


def test_scene_retry_does_not_repeat_completed_translation():
    with msv.demo["pentalanine"] as source:
        with msv.MolSysView(transport=InterruptedWidget()) as view:
            view.load(source.molsys, structure_indices=[0, 8, 3])
            view.shapes.add_sphere(atom_indices=[0], tag="anchor")
            before = values(view).copy()
            view._ready = True
            view.widget.interrupted = True
            with pytest.raises(SystemEditSyncError) as error:
                view.addons.molsysmt.structure.translate(
                    translation="[1, 0, 0] nm", in_place=True
                )
            assert (
                error.value.science_completed is True
                and error.value.scientific_result is None
            )
            assert isinstance(error.value.__cause__, OSError)
            assert view.addons.molsysmt.get_sync_status()["state"] == "sync_failed"
            expected = before + [1, 0, 0]
            np.testing.assert_allclose(values(view), expected)
            storage = view.molsys.structures._coordinates
            view.addons.molsysmt.sync_view()
            np.testing.assert_allclose(values(view), expected)
            assert view.molsys.structures._coordinates is storage
            assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1


def test_postpublication_scientific_interruption_is_uncertain(view):
    from molsysviewer_molsysmt._geometry import (
        _geometry_token,
        _prepare_geometry_transform,
    )

    before = values(view).copy()

    def prepare(target):
        plan = _prepare_geometry_transform(
            target,
            "translate",
            dict(
                translation=puw.quantity([1, 0, 0], "nm"),
                selection="all",
                structure_indices="all",
                syntax="MolSysMT",
                in_place=True,
                skip_digestion=False,
            ),
        )
        native_run = plan["run"]

        def run():
            native_run()
            raise RuntimeError("interruption after native translation")

        plan["run"] = run
        return plan

    with pytest.raises(RuntimeError, match="after native translation"):
        view.addons.manager.system_edits.execute(
            prepare, name="receiving.translate", rejection_check=_geometry_token
        )
    np.testing.assert_allclose(values(view), before + [1, 0, 0])
    assert view.addons.molsysmt.get_sync_status()["state"] == "uncertain"
    with pytest.raises(SystemEditPendingError):
        view.addons.molsysmt.sync_view()
