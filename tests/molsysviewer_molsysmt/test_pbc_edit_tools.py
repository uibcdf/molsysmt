"""Receive periodic edits with lattice truth and real-view effect ownership."""

import inspect
import itertools

import molsysviewer as msv
import numpy as np
import pytest
from molsysviewer.system_edits import SystemEditPendingError, SystemEditSyncError
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm

puw = msm.pyunitwizard
EDITORS = ("wrap_to_pbc", "wrap_to_mic", "unwrap")
ATOMS = [7, 1, 4, 9]
SCOPE = [2, 0, 2]
SHIFTS = np.array(list(itertools.product(range(-2, 3), repeat=3)))


def xyz(molsys):
    return puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm").copy()


def cell(skew=False):
    return np.array(
        [
            [3.0, 0, 0],
            [0.7 if skew else 0, 4.0, 0],
            [0.2 if skew else 0, 0.6 if skew else 0, 5.0],
        ]
    )


def nearest(vectors, box):
    """Exhaustive nearby lattice oracle for the bounded, mildly skew test cells."""
    base = np.rint(vectors @ np.linalg.inv(box))
    candidates = vectors[:, None] - (base[:, None] + SHIFTS[None]) @ box
    norm2 = np.sum(candidates**2, axis=-1)
    return candidates[np.arange(len(vectors)), np.argmin(norm2, axis=1)]


def wrapped(points, box, method, origin=None, centered=False):
    origin = np.zeros(3) if origin is None else np.asarray(origin)
    relative = points - origin
    if method == "wrap_to_mic":
        return origin + nearest(relative, box)
    frac = relative @ np.linalg.inv(box)
    return origin + (frac - np.floor(frac + (0.5 if centered else 0))) @ box


def fresh_analysis(view):
    if "science" in view.molsys.interactions:
        view.interactions.delete_analysis("science")
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=view.molsys.get_n_atoms(),
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="receiving.pbc.edits",
    )
    view.interactions.attach(analysis, name="science", assume_aligned=True)


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            values = xyz(result.molsys)
            msm.set(
                result.molsys,
                coordinates=puw.quantity(values + [8.0, 7.0, 6.0], "nm"),
                box=puw.quantity(np.tile(cell(), (3, 1, 1)), "nm"),
            )
            analysis = msm.Interactions.from_records(
                [],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.pbc.edits",
            )
            result.interactions.attach(analysis, name="science", assume_aligned=True)
            yield result


@pytest.mark.parametrize("name", EDITORS)
def test_native_scientific_signature_defaults_and_effect_help(view, name):
    native = inspect.signature(getattr(msm.pbc, name))
    bound = getattr(view.addons.molsysmt.pbc, name)
    expected = list(native.parameters.values())[1:]
    expected.append(
        inspect.Parameter("update_view", inspect.Parameter.KEYWORD_ONLY, default=True)
    )
    assert inspect.signature(bound) == native.replace(parameters=expected)
    assert bound.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, name)
    doc = inspect.getdoc(bound)
    assert "native in_place=False default" in doc
    assert "molecular edit, box assignment" not in doc
    assert "no minimum-image algorithm" in doc
    if name == "unwrap":
        assert "supplied structure order" in doc
    else:
        assert inspect.signature(bound).parameters["compact"].default == "component"
        assert "rejected before scientific writes" in doc


@pytest.mark.parametrize("name", EDITORS[:2])
@pytest.mark.parametrize("skew", [False, True])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_atomwise_wrap_lattice_truth_units_order_and_native_ownership(
    view, name, skew, in_place, unit
):
    box = cell(skew)
    msm.set(view.molsys, box=puw.quantity(np.tile(box, (3, 1, 1)), "nm"))
    fresh_analysis(view)
    before, state, target = xyz(view.molsys), view.export_state(), view.molsys
    options = dict(
        selection=ATOMS, structure_indices=SCOPE, compact=False, in_place=in_place
    )
    native_target = msm.copy(target)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        native_result = getattr(msm.pbc, name)(native_target, **options)
        result = getattr(view.addons.molsysmt.pbc, name)(**options)
    output = target if in_place else result
    assert result is None if in_place else result is not target
    expected = before.copy()
    for s in set(SCOPE):
        expected[s, ATOMS] = wrapped(before[s, ATOMS], box, name)
    np.testing.assert_allclose(xyz(output), expected, atol=2e-12, rtol=0)
    np.testing.assert_allclose(
        xyz(output), xyz(native_target if in_place else native_result), atol=2e-12
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(output, box=True), to_unit="nm"), np.tile(box, (3, 1, 1))
    )
    assert view.molsys is target
    if in_place:
        np.testing.assert_array_equal(
            target.interactions["science"].evaluated_structure_indices, [1]
        )
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1
    else:
        np.testing.assert_array_equal(xyz(target), before)
        assert view.export_state() == state
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0
        assert (
            output.structures is not target.structures
            and output.topology is not target.topology
        )


@pytest.mark.parametrize("skew", [False, True])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("centered", [False, True])
def test_explicit_origin_and_center_are_native_periodic_cell_parameters(
    view, skew, in_place, centered
):
    box, origin = cell(skew), np.array([0.2, -0.4, 0.7])
    msm.set(view.molsys, box=puw.quantity(np.tile(box, (3, 1, 1)), "nm"))
    before = xyz(view.molsys)
    option = {
        "box_center" if centered else "box_origin": puw.quantity(
            origin * 10, "angstrom"
        )
    }
    result = view.addons.molsysmt.pbc.wrap_to_pbc(
        selection=ATOMS,
        structure_indices=[2, 0],
        compact=False,
        in_place=in_place,
        **option,
    )
    expected = before.copy()
    for s in [2, 0]:
        expected[s, ATOMS] = wrapped(
            before[s, ATOMS], box, "wrap_to_pbc", origin, centered
        )
    np.testing.assert_allclose(
        xyz(view.molsys if in_place else result), expected, atol=3e-12, rtol=0
    )


@pytest.mark.parametrize("name", EDITORS[:2])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_centered_independent_output_preserves_input_and_weighted_centering(
    view, name, unit
):
    before = xyz(view.molsys)
    moving, fitting = [0, 1, 2, 3], [0, 1]
    destination, weights = np.array([0.2, 0.3, 0.4]), np.array([1.0, 3.0])
    origin = np.array([0.1, -0.2, 0.3])
    option = {
        "box_origin" if name == "wrap_to_pbc" else "mic_origin": puw.quantity(
            origin, "nm"
        )
    }
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = getattr(view.addons.molsysmt.pbc, name)(
            selection=moving,
            center_of_selection=fitting,
            weights=weights,
            center_coordinates=puw.quantity(destination, "nm"),
            structure_indices=[2, 0],
            compact=False,
            **option,
        )
    expected = before.copy()
    for s in [2, 0]:
        center = np.average(before[s, fitting], axis=0, weights=weights)
        shifted = before[s, moving] + destination - center
        expected[s, moving] = wrapped(shifted, cell(), name, origin)
    np.testing.assert_allclose(xyz(result), expected, atol=3e-12, rtol=0)
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


@pytest.mark.parametrize("name", EDITORS[:2])
@pytest.mark.parametrize("skew", [False, True])
@pytest.mark.parametrize("in_place", [False, True])
def test_component_wrapping_reconstructs_actual_peptide_geometry(
    view, name, skew, in_place
):
    box = cell(skew)
    original = xyz(view.molsys)
    split = np.stack([wrapped(points, box, "wrap_to_pbc") for points in original])
    msm.set(
        view.molsys,
        coordinates=puw.quantity(split, "nm"),
        box=puw.quantity(np.tile(box, (3, 1, 1)), "nm"),
    )
    # Reattach evaluated coverage after deliberately preparing split coordinates.
    current = view.molsys.interactions["science"]
    assert len(current.evaluated_structure_indices) == 0
    topology = view.molsys.topology
    result = getattr(view.addons.molsysmt.pbc, name)(in_place=in_place)
    after = xyz(view.molsys if in_place else result)
    for s in range(3):
        np.testing.assert_allclose(
            after[s] - after[s, 0], original[s] - original[s, 0], atol=3e-12
        )
        center = original[s].mean(axis=0)
        expected_center = wrapped(center[None], box, name)[0]
        np.testing.assert_allclose(after[s].mean(axis=0), expected_center, atol=3e-12)
    assert view.molsys.topology is topology
    if not in_place:
        np.testing.assert_array_equal(xyz(view.molsys), split)


@pytest.mark.parametrize("skew", [False, True])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("scope", [[0, 1, 2], [2, 0, 2]])
def test_unwrap_temporal_order_is_distinct_from_covalent_reconstruction(
    view, skew, in_place, unit, scope
):
    box = cell(skew)
    original = xyz(view.molsys)
    offsets = np.array([[0.1, 0.1, 0.1], [0.7, 0.15, 0.2], [0.9, 0.2, 0.3]]) @ box
    data = original - original[:, :1] + offsets[:, None]
    data = np.stack([wrapped(points, box, "wrap_to_pbc") for points in data])
    msm.set(
        view.molsys,
        coordinates=puw.quantity(data, "nm"),
        box=puw.quantity(np.tile(box, (3, 1, 1)), "nm"),
    )
    expected = data.copy()
    selected = data[scope][:, ATOMS].copy()
    for i in range(1, len(scope)):
        selected[i] = selected[i - 1] + nearest(selected[i] - selected[i - 1], box)
    for i, s in enumerate(scope):
        expected[s, ATOMS] = selected[i]
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = view.addons.molsysmt.pbc.unwrap(
            selection=ATOMS, structure_indices=scope, in_place=in_place
        )
    np.testing.assert_allclose(
        xyz(view.molsys if in_place else result), expected, atol=4e-12, rtol=0
    )
    if not in_place:
        np.testing.assert_array_equal(xyz(view.molsys), data)


@pytest.mark.parametrize("name", EDITORS[:2])
@pytest.mark.parametrize("skip", [False, True])
def test_unreceived_centered_in_place_rejects_before_any_scientific_or_scene_write(
    view, name, skip
):
    before, state = xyz(view.molsys), view.export_state()
    status = view.addons.molsysmt.get_sync_status()
    analysis = view.molsys.interactions["science"]
    with pytest.raises(NotImplementedError, match="detached copy"):
        getattr(view.addons.molsysmt.pbc, name)(
            center_of_selection=[0, 1], in_place=True, skip_digestion=skip
        )
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )
    assert view.molsys.interactions["science"] is analysis


@pytest.mark.parametrize("name", EDITORS)
@pytest.mark.parametrize(
    "arguments",
    [
        {"selection": [99999]},
        {"structure_indices": [99999]},
        {"engine": "unknown"},
    ],
)
def test_native_prewrite_rejections_preserve_science_and_clean_sync_state(
    view, name, arguments
):
    before, state = xyz(view.molsys), view.export_state()
    native = msm.copy(view.molsys)
    with pytest.raises(Exception) as error:
        getattr(msm.pbc, name)(native, in_place=True, **arguments)
    with pytest.raises(type(error.value)):
        getattr(view.addons.molsysmt.pbc, name)(in_place=True, **arguments)
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("name", EDITORS)
def test_missing_box_is_native_error_without_coordinate_publication(view, name):
    msm.set(view.molsys, box=None)
    before = xyz(view.molsys)
    with pytest.raises(Exception) as error:
        getattr(msm.pbc, name)(msm.copy(view.molsys), in_place=True)
    with pytest.raises(type(error.value)):
        getattr(view.addons.molsysmt.pbc, name)(in_place=True)
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


def test_deferred_pbc_and_structure_edits_compose_and_preserve_scene_owners(view):
    tools, target = view.addons.molsysmt, view.molsys
    region = view.regions.add(selection=[0, 2, 4], tag="region")
    saved = view.selections.add("saved", atom_indices=[0, 2])
    sphere = view.shapes.add_sphere(atom_indices=[2], tag="anchor")
    view.active_selection.set([0, 2])
    view.player.go_to_structure(2)
    source_id = view.load_blocks[0]["source_id"]
    tools.pbc.wrap_to_pbc(structure_indices=[2], in_place=True, update_view=False)
    tools.structure.translate(
        translation="[.2, 0, 0] nm",
        selection=[0, 2],
        structure_indices=[0],
        in_place=True,
        update_view=False,
    )
    final = xyz(target)
    assert tools.get_sync_status()["pending_operations"] == 2
    assert tools.pbc.has_pbc() is True
    with pytest.raises(SystemEditPendingError):
        view.export_state()
    tools.sync_view()
    np.testing.assert_array_equal(xyz(target), final)
    assert view.molsys is target and view.regions["region"] is region
    assert view.selections["saved"] is saved and view.shapes["anchor"] is sphere
    assert view.active_selection.atom_indices == [0, 2] and view.player.index == 2
    assert view.load_blocks[0]["source_id"] == source_id
    np.testing.assert_array_equal(
        target.interactions["science"].evaluated_structure_indices, [1]
    )
    assert tools.get_sync_status()["target_revision"] == 2


class InterruptedWidget(MolSysViewerWidget):
    interrupted = False

    def send(self, content, buffers=None):
        if self.interrupted and content.get("op") == "add_sphere":
            self.interrupted = False
            raise OSError("receiving periodic edit connector interruption")
        return super().send(content, buffers=buffers)


def test_scene_retry_does_not_replay_completed_periodic_edit():
    with msv.demo["pentalanine"] as source:
        with msv.MolSysView(transport=InterruptedWidget()) as view:
            view.load(source.molsys, structure_indices=[0, 8, 3])
            msm.set(view.molsys, box=puw.quantity(np.tile(cell(), (3, 1, 1)), "nm"))
            view.shapes.add_sphere(atom_indices=[0], tag="anchor")
            view._ready = True
            view.widget.interrupted = True
            with pytest.raises(SystemEditSyncError) as error:
                view.addons.molsysmt.pbc.wrap_to_mic(in_place=True)
            assert (
                error.value.science_completed is True
                and error.value.scientific_result is None
            )
            final, storage = xyz(view.molsys), view.molsys.structures._coordinates
            view.addons.molsysmt.sync_view()
            np.testing.assert_array_equal(xyz(view.molsys), final)
            assert view.molsys.structures._coordinates is storage
            assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1


@pytest.mark.parametrize("name", EDITORS)
def test_cached_editor_lifetime_and_closed_primary_guards(name):
    with msv.new_view() as view:
        method = getattr(view.addons.molsysmt.pbc, name)
        with pytest.raises(ValueError, match="Load a molecular system"):
            method()
    with pytest.raises(RuntimeError, match="closed view"):
        method(skip_digestion=True)
