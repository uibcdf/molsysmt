"""Receive native fits with independent poses and real scene/lifecycle boundaries."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from molsysviewer.system_edits import SystemEditPendingError, SystemEditSyncError
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm
from molsysmt.native import Structures

puw = msm.pyunitwizard
TOOLS = ("least_rmsd_fit", "least_rmsd_align")
SCOPE = [2, 0, 2]


def xyz(molsys):
    return puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm")


def pose(points, turn, shift):
    result = points.copy()
    x, y = points[:, 0], points[:, 1]
    if turn == 1:
        result[:, 0], result[:, 1] = -y, x
    elif turn == 2:
        result[:, 0], result[:, 1] = -x, -y
    return result + shift


@pytest.fixture
def fitted_scene():
    with msv.demo["pentalanine"] as source:
        reference = msm.extract(source.molsys, structure_indices=[0, 8, 3])
        base = xyz(reference)[1].copy()
        query = msm.copy(reference)
        coordinates = np.stack(
            [
                pose(base, 1, [1.2, -0.3, 0.6]),
                pose(base, 0, [-0.5, 0.4, 0.2]),
                pose(base, 2, [0.3, 1.4, -0.8]),
            ]
        )
        msm.set(
            query,
            coordinates=puw.quantity(coordinates, "nm"),
            box=puw.quantity(np.tile(np.eye(3) * 3, (3, 1, 1)), "nm"),
        )
        with msv.new_view(query) as view:
            analysis = msm.interactions.hbonds.get_buch_hbonds(
                view.molsys,
                structure_indices="all",
                pbc=False,
                output_type="molsysmt.Interactions",
            )
            view.interactions.attach(analysis, name="science", assume_aligned=True)
            view.interactions.add("science", tag="hb")
            yield view, reference, base


@pytest.mark.parametrize("name", TOOLS)
def test_signatures_defaults_native_help_and_explicit_namespace(fitted_scene, name):
    view, _, _ = fitted_scene
    native = inspect.signature(getattr(msm.structure, name))
    bound = getattr(view.addons.molsysmt.structure, name)
    parameters = inspect.signature(bound).parameters
    assert [p for n, p in parameters.items() if n != "update_view"] == list(
        native.parameters.values()
    )[1:]
    assert parameters["in_place"].default is False
    assert parameters["reference_molecular_system"].default is None
    assert parameters["update_view"].kind is inspect.Parameter.KEYWORD_ONLY
    assert parameters["update_view"].default is True
    assert bound.digestion_plan is not None
    assert set(TOOLS) <= set(dir(view.addons.molsysmt.structure))
    assert not hasattr(view.addons.molsysmt, name)
    doc = inspect.getdoc(bound)
    assert "native in_place=False default" in doc
    assert "No molecular edit" not in doc
    assert "caller-owned" in doc
    if name == "least_rmsd_align":
        assert "complete selected components" in doc
        assert "#452" in doc and "#453" in doc
        assert "fails before" not in doc
        assert "incorrectly interpreted" not in doc


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("moving", ["all", [1, 3, 5, 7, 9, 11]])
def test_fit_analytical_pose_selected_moving_atoms_and_structure_order(
    fitted_scene, unit, in_place, moving
):
    view, reference, base = fitted_scene
    target, state = view.molsys, view.export_state()
    before, reference_before = xyz(target).copy(), xyz(reference).copy()
    analysis = target.interactions["science"]
    anchors = msm.select(target, selection="atom_name=='CA'")[::-1]
    expected = before.copy()
    atoms = list(range(len(base))) if moving == "all" else moving
    expected[np.ix_([0, 2], atoms)] = base[atoms]
    box = puw.get_value(msm.get(target, box=True), to_unit="nm").copy()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = view.addons.molsysmt.structure.least_rmsd_fit(
            selection=moving,
            selection_fit=anchors,
            structure_indices=SCOPE,
            reference_molecular_system=reference,
            reference_selection_fit=anchors,
            reference_structure_index=1,
            in_place=in_place,
            use_gpu=False,
            precision="double",
        )
    output = target if in_place else result
    assert result is None if in_place else result is not target
    assert view.molsys is target
    np.testing.assert_allclose(xyz(output), expected, rtol=0, atol=1e-11)
    np.testing.assert_array_equal(xyz(reference), reference_before)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(output, box=True), to_unit="nm"), box
    )
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1, 2])
    np.testing.assert_array_equal(
        output.interactions["science"].evaluated_structure_indices, [1]
    )
    if not in_place:
        np.testing.assert_array_equal(xyz(target), before)
        assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("in_place", [False, True])
def test_sequence_align_analytical_coordinates_and_external_reference_ownership(
    fitted_scene, unit, in_place
):
    view, reference, base = fitted_scene
    target, state = view.molsys, view.export_state()
    before, reference_before = xyz(target).copy(), xyz(reference).copy()
    old_analysis = target.interactions["science"]
    expected = before.copy()
    expected[[0, 2]] = base
    box = puw.get_value(msm.get(target, box=True), to_unit="nm").copy()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = view.addons.molsysmt.structure.least_rmsd_align(
            structure_indices=SCOPE,
            reference_molecular_system=reference,
            reference_structure_index=1,
            in_place=in_place,
            use_gpu=False,
            precision="double",
        )
    output = target if in_place else result
    assert result is None if in_place else result is not target
    np.testing.assert_allclose(xyz(output), expected, rtol=0, atol=1e-11)
    np.testing.assert_array_equal(xyz(reference), reference_before)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(output, box=True), to_unit="nm"), box
    )
    np.testing.assert_array_equal(old_analysis.evaluated_structure_indices, [0, 1, 2])
    np.testing.assert_array_equal(
        output.interactions["science"].evaluated_structure_indices, [1]
    )
    if not in_place:
        np.testing.assert_array_equal(xyz(target), before)
        assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("reference_mode", ["omitted", "self"])
def test_native_fit_self_reference_is_preserved_without_adoption(
    fitted_scene, reference_mode
):
    view, _, _ = fitted_scene
    target, state = view.molsys, view.export_state()
    before = xyz(target).copy()
    extra = (
        {} if reference_mode == "omitted" else {"reference_molecular_system": target}
    )
    output = view.addons.molsysmt.structure.least_rmsd_fit(
        selection_fit="all",
        structure_indices=SCOPE,
        reference_structure_index=1,
        use_gpu=False,
        update_view=False,
        **extra,
    )
    expected = before.copy()
    expected[[0, 2]] = before[1]
    np.testing.assert_allclose(xyz(output), expected, rtol=0, atol=1e-11)
    np.testing.assert_array_equal(xyz(target), before)
    assert view.molsys is target and output is not target
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


def test_fit_separate_atom_correspondence_and_native_structures_reference(fitted_scene):
    view, reference, base = fitted_scene
    count = len(base)
    order = list(range(count - 1, -1, -1))
    # MolSys atom extraction retains sorted indices; use an explicitly ordered
    # coordinate-only reference rather than assuming extraction is a permutation.
    reordered = Structures(coordinates=puw.quantity(xyz(reference)[:, order], "nm"))
    np.testing.assert_array_equal(xyz(reordered), xyz(reference)[:, order])
    output = view.addons.molsysmt.structure.least_rmsd_fit(
        selection_fit=[0, 2, 4, 6],
        structure_indices=[2, 0],
        reference_molecular_system=reordered,
        reference_selection_fit=[count - 1 - i for i in [0, 2, 4, 6]],
        reference_structure_index=1,
        use_gpu=False,
    )
    np.testing.assert_allclose(xyz(output)[[0, 2]], [base, base], rtol=0, atol=1e-11)
    # A coordinate-only native reference keeps a distinct physical length unit.
    anchors = msm.select(reference, selection="atom_name=='CA'")
    coordinates = puw.quantity(base[anchors][None] * 10, "angstrom")
    external = Structures(coordinates=coordinates)
    external.coordinates = coordinates
    unchanged = puw.get_value(external.coordinates).copy()
    output = view.addons.molsysmt.structure.least_rmsd_fit(
        selection_fit=anchors,
        structure_indices=[0, 2],
        reference_molecular_system=external,
        reference_selection_fit=list(range(len(anchors))),
        use_gpu=False,
    )
    np.testing.assert_allclose(xyz(output)[[0, 2]], [base, base], rtol=0, atol=1e-11)
    np.testing.assert_array_equal(puw.get_value(external.coordinates), unchanged)


@pytest.mark.parametrize("to_form", ["molsysmt.MolSys", "molsysmt.Structures"])
def test_fit_native_independent_output_form_is_not_adopted(fitted_scene, to_form):
    view, reference, base = fitted_scene
    before, state = xyz(view.molsys).copy(), view.export_state()
    result = view.addons.molsysmt.structure.least_rmsd_fit(
        reference_molecular_system=reference,
        reference_structure_index=1,
        to_form=to_form,
        use_gpu=False,
    )
    assert msm.get_form(result) == to_form
    np.testing.assert_allclose(
        xyz(result), np.tile(base[None], (3, 1, 1)), rtol=0, atol=1e-11
    )
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.export_state() == state


@pytest.mark.parametrize("name", TOOLS)
def test_cpu_single_precision_keeps_native_values_and_reference(fitted_scene, name):
    view, reference, base = fitted_scene
    original = xyz(reference).copy()
    result = getattr(view.addons.molsysmt.structure, name)(
        reference_molecular_system=reference,
        reference_structure_index=1,
        precision="single",
        use_gpu=False,
    )
    np.testing.assert_allclose(
        xyz(result), np.tile(base[None], (3, 1, 1)), rtol=0, atol=2e-6
    )
    np.testing.assert_array_equal(xyz(reference), original)


def test_sequence_alignment_moves_selected_component_beyond_anchors(fitted_scene):
    view, reference, base = fitted_scene
    first = msm.extract(view.molsys, structure_indices=[0])
    second = msm.extract(reference, structure_indices=[1])
    second_before = xyz(second).copy() + [8, 0, 0]
    msm.set(second, coordinates=puw.quantity(second_before, "nm"))
    first.interactions = {}
    second.interactions = {}
    merged = msm.merge([first, second])
    n_atoms = len(base)
    with msv.new_view(merged) as combined:
        before = xyz(combined.molsys).copy()
        selected = msm.select(
            combined.molsys, selection=f"atom_index<{n_atoms} and atom_name=='CA'"
        )
        assert len(selected) >= 3 and len(selected) < n_atoms
        combined.addons.molsysmt.structure.least_rmsd_align(
            selection=f"atom_index<{n_atoms} and atom_name=='CA'",
            reference_molecular_system=reference,
            reference_structure_index=1,
            in_place=True,
            use_gpu=False,
        )
        observed = xyz(combined.molsys)
        np.testing.assert_allclose(observed[0, :n_atoms], base, rtol=0, atol=1e-11)
        np.testing.assert_array_equal(observed[:, n_atoms:], before[:, n_atoms:])


@pytest.mark.parametrize(
    "name, arguments",
    [
        ("least_rmsd_fit", {"selection_fit": [0, 0, 0]}),
        ("least_rmsd_fit", {"reference_selection_fit": [0, 1]}),
        ("least_rmsd_fit", {"engine": "unknown"}),
        ("least_rmsd_fit", {"selection": [99999]}),
        ("least_rmsd_align", {"engine_sequence_alignment": "unknown"}),
        ("least_rmsd_align", {"engine_least_rmsd_fit": "unknown"}),
        ("least_rmsd_align", {"reference_structure_index": 99999}),
        ("least_rmsd_align", {"structure_indices": [99999]}),
    ],
)
def test_native_fit_rejections_preserve_source_scene_and_status(
    fitted_scene, name, arguments
):
    view, reference, _ = fitted_scene
    native = msm.copy(view.molsys)
    before, state, reference_before = (
        xyz(view.molsys).copy(),
        view.export_state(),
        xyz(reference).copy(),
    )
    analysis = view.molsys.interactions["science"]
    parameters = dict(
        reference_molecular_system=reference, use_gpu=False, in_place=True, **arguments
    )
    with pytest.raises(Exception) as error:
        getattr(msm.structure, name)(native, **parameters)
    with pytest.raises(type(error.value)):
        getattr(view.addons.molsysmt.structure, name)(**parameters)
    np.testing.assert_array_equal(xyz(view.molsys), before)
    np.testing.assert_array_equal(xyz(reference), reference_before)
    assert view.export_state() == state
    assert view.molsys.interactions["science"] is analysis
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("name", TOOLS)
@pytest.mark.parametrize("controls", [{"in_place": "yes"}, {"update_view": 1}])
def test_fit_integration_controls_survive_skipped_digestion(
    fitted_scene, name, controls
):
    view, reference, _ = fitted_scene
    before, state = xyz(view.molsys).copy(), view.export_state()
    with pytest.raises(Exception):
        getattr(view.addons.molsysmt.structure, name)(
            reference_molecular_system=reference,
            skip_digestion=True,
            **controls,
        )
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.export_state() == state


def test_fits_compose_pending_edits_and_keep_scene_identity(fitted_scene):
    view, reference, base = fitted_scene
    tools = view.addons.molsysmt
    region = view.regions.add(selection=[2, 4], tag="kept")
    saved = view.selections.add("saved", atom_indices=[2, 4])
    sphere = view.shapes.add_sphere(atom_indices=[4], tag="anchor")
    view.active_selection.set([2, 4])
    view.player.go_to_structure(2)
    source = dict(view.load_blocks[0])
    ref_before = xyz(reference).copy()
    tools.structure.translate(
        translation="[0,0,1] nm", in_place=True, update_view=False
    )
    tools.structure.least_rmsd_fit(
        reference_molecular_system=reference,
        reference_structure_index=1,
        in_place=True,
        update_view=False,
        use_gpu=False,
    )
    assert tools.get_sync_status()["pending_operations"] == 2
    with pytest.raises(SystemEditPendingError):
        region.hide(skip_digestion=True)
    # This independent fit reads pending science and changes no projection state.
    result = tools.structure.least_rmsd_align(
        reference_molecular_system=reference,
        reference_structure_index=1,
        update_view=False,
        use_gpu=False,
    )
    np.testing.assert_allclose(
        xyz(result), np.tile(base[None], (3, 1, 1)), rtol=0, atol=1e-11
    )
    assert tools.get_sync_status()["pending_operations"] == 2
    tools.structure.least_rmsd_align(
        reference_molecular_system=reference,
        reference_structure_index=1,
        in_place=True,
        update_view=False,
        use_gpu=False,
    )
    storage = view.molsys.structures._coordinates
    tools.sync_view()
    np.testing.assert_allclose(
        xyz(view.molsys), np.tile(base[None], (3, 1, 1)), rtol=0, atol=1e-11
    )
    np.testing.assert_array_equal(xyz(reference), ref_before)
    assert view.molsys.structures._coordinates is storage
    assert view.regions["kept"] is region and region.atom_indices == (2, 4)
    assert view.selections["saved"] is saved and saved.atom_indices == [2, 4]
    assert view.shapes["anchor"] is sphere
    assert view.active_selection.atom_indices == [2, 4] and view.player.index == 2
    assert view.load_blocks[0]["source_id"] == source["source_id"]
    assert tools.get_sync_status()["target_revision"] == 3
    assert not view.history.can_undo()


@pytest.mark.parametrize("name", TOOLS)
def test_borrowed_reference_view_is_not_adopted_or_synchronized(fitted_scene, name):
    view, reference, base = fitted_scene
    with msv.new_view(reference) as other:
        other.addons.molsysmt.structure.translate(
            translation="[0,0,1] nm", in_place=True, update_view=False
        )
        before = xyz(other.molsys).copy()
        status = other.addons.molsysmt.get_sync_status()
        result = getattr(view.addons.molsysmt.structure, name)(
            reference_molecular_system=other.molsys,
            reference_structure_index=1,
            use_gpu=False,
        )
        np.testing.assert_allclose(
            xyz(result),
            np.tile((base + [0, 0, 1])[None], (3, 1, 1)),
            rtol=0,
            atol=1e-11,
        )
        np.testing.assert_array_equal(xyz(other.molsys), before)
        assert other.addons.molsysmt.get_sync_status() == status
        assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("name", TOOLS)
def test_cached_fit_uses_replacement_and_rejects_closed_or_empty_views(
    fitted_scene, name
):
    view, reference, base = fitted_scene
    method = getattr(view.addons.molsysmt.structure, name)
    replacement = msm.copy(view.molsys)
    msm.set(replacement, coordinates=puw.quantity(xyz(replacement) + [2, 0, 0], "nm"))
    view.load(replacement, mode="replace")
    before = xyz(view.molsys).copy()
    method(
        reference_molecular_system=reference,
        reference_structure_index=1,
        in_place=True,
        use_gpu=False,
    )
    assert not np.array_equal(xyz(view.molsys), before)
    np.testing.assert_allclose(
        xyz(view.molsys), np.tile(base[None], (3, 1, 1)), rtol=0, atol=1e-11
    )
    with pytest.raises(TypeError):
        method(molecular_system=reference, skip_digestion=True)
    view.close()
    with pytest.raises(RuntimeError, match="closed"):
        method(reference_molecular_system=reference, in_place=True, use_gpu=False)
    with msv.MolSysView() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.structure, name)(
                reference_molecular_system=reference, use_gpu=False
            )


class InterruptedFitWidget(MolSysViewerWidget):
    interrupted = False

    def send(self, content, buffers=None):
        if self.interrupted and content.get("op") == "add_sphere":
            self.interrupted = False
            raise OSError("fit receiving transport interruption")
        return super().send(content, buffers=buffers)


@pytest.mark.parametrize("name", TOOLS)
def test_completed_fit_scene_retry_has_no_second_scientific_write(fitted_scene, name):
    source, reference, base = fitted_scene
    with msv.MolSysView(transport=InterruptedFitWidget()) as view:
        view.load(source.molsys)
        view.shapes.add_sphere(atom_indices=[0], tag="anchor")
        view._ready = True
        view.widget.interrupted = True
        with pytest.raises(SystemEditSyncError) as error:
            getattr(view.addons.molsysmt.structure, name)(
                reference_molecular_system=reference,
                reference_structure_index=1,
                in_place=True,
                use_gpu=False,
            )
        assert error.value.science_completed is True
        assert error.value.scientific_result is None
        assert isinstance(error.value.__cause__, OSError)
        storage = view.molsys.structures._coordinates
        view.addons.molsysmt.sync_view()
        assert view.molsys.structures._coordinates is storage
        np.testing.assert_allclose(
            xyz(view.molsys), np.tile(base[None], (3, 1, 1)), rtol=0, atol=1e-11
        )
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1


@pytest.mark.parametrize("name", TOOLS)
def test_fit_pipeline_interruption_after_publication_enters_uncertain_state(
    fitted_scene, name
):
    from molsysviewer_molsysmt._geometry import (
        _geometry_token,
        _prepare_geometry_transform,
    )

    view, reference, base = fitted_scene

    def prepare(target):
        plan = _prepare_geometry_transform(
            target,
            name,
            {
                "selection": "all" if name == "least_rmsd_fit" else "atom_name=='CA'",
                "structure_indices": "all",
                "syntax": "MolSysMT",
                "in_place": True,
                "reference_molecular_system": reference,
                "reference_structure_index": 1,
                "use_gpu": False,
            },
        )
        native_run = plan["run"]

        def interrupted_pipeline():
            native_run()
            raise RuntimeError("interruption after native fit publication")

        plan["run"] = interrupted_pipeline
        return plan

    with pytest.raises(RuntimeError, match="after native fit publication"):
        view.addons.manager.system_edits.execute(
            prepare,
            name=f"receiving.{name}",
            rejection_check=_geometry_token,
        )
    np.testing.assert_allclose(
        xyz(view.molsys), np.tile(base[None], (3, 1, 1)), rtol=0, atol=1e-11
    )
    assert view.addons.molsysmt.get_sync_status()["state"] == "uncertain"
    with pytest.raises(SystemEditPendingError):
        view.addons.molsysmt.sync_view()


@pytest.mark.parametrize("reference_mode", ["omitted", "none", "self"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("selection_kind", ["indices", "mask"])
def test_sequence_alignment_receives_native_self_reference_and_atom_axes(
    fitted_scene, reference_mode, in_place, selection_kind
):
    view, _, _ = fitted_scene
    target = view.molsys
    before, state = xyz(target).copy(), view.export_state()
    atoms = msm.select(target, selection='atom_name=="CA"')
    selection = atoms[::-1]
    if selection_kind == "mask":
        selection = np.zeros(len(before[0]), dtype=bool)
        selection[atoms] = True
    extra = (
        {}
        if reference_mode == "omitted"
        else {
            "reference_molecular_system": None if reference_mode == "none" else target
        }
    )
    result = view.addons.molsysmt.structure.least_rmsd_align(
        selection=selection,
        structure_indices=SCOPE,
        reference_structure_index=1,
        use_gpu=False,
        in_place=in_place,
        **extra,
    )
    expected = before.copy()
    expected[[0, 2]] = before[1]
    output = target if in_place else result
    assert (result is None) == in_place
    np.testing.assert_allclose(xyz(output), expected, rtol=0, atol=1e-11)
    assert view.molsys is target
    if not in_place:
        np.testing.assert_array_equal(xyz(target), before)
        assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
