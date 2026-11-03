"""Receive native torsion editors with quaternion and periodic-image references."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from molsysviewer.system_edits import SystemEditPendingError, SystemEditSyncError
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm

puw = msm.pyunitwizard
TOOLS = ("set_dihedral_angles", "shift_dihedral_angles")
SCOPE = [2, 0, 2]


def xyz(molsys):
    return puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm")


def command(method, value):
    return {"angles" if method == "set_dihedral_angles" else "shifts": value}


def quartets(molsys):
    return np.asarray(
        msm.chemical_states.get_dihedral_quartets(molsys, phi=True), dtype=np.int64
    )[:2]


def blocks_for(molsys, q):
    return next(
        block
        for block in msm.chemical_states.get_covalent_blocks(
            molsys, remove_bonds=q[1:3]
        )
        if q[3] in block
    )


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            msm.set(
                result.molsys,
                box=puw.quantity(np.tile(np.eye(3) * 20, (3, 1, 1)), "nm"),
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


def mic(vector, box):
    if box is None:
        return vector
    frac = vector @ np.linalg.inv(box)
    return (frac - np.floor(frac + 0.5)) @ box


def torsion(points, box=None):
    a = mic(points[0] - points[1], box)
    axis = mic(points[2] - points[1], box)
    axis = axis / np.linalg.norm(axis)
    b = mic(points[3] - points[2], box)
    a = a - np.dot(a, axis) * axis
    b = b - np.dot(b, axis) * axis
    return np.arctan2(np.dot(np.cross(axis, a), b), np.dot(a, b))


def rotated(points, quartet, block, target, box=None):
    out = points.copy()
    j, k = quartet[1:3]
    axis = mic(points[k] - points[j], box)
    axis = axis / np.linalg.norm(axis)
    delta = target - torsion(points[quartet], box)
    w = np.cos(delta / 2)
    x, y, z = axis * np.sin(delta / 2)
    matrix = np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
        ]
    )
    block = np.array(sorted(block), dtype=int)
    relative = mic(points[block] - points[k], box)
    out[block] = points[k] + mic(relative @ matrix.T, box)
    return out


@pytest.mark.parametrize("name", TOOLS)
def test_scientific_signature_controls_help_and_module_path(view, name):
    method = getattr(view.addons.molsysmt.structure, name)
    native = inspect.signature(getattr(msm.structure, name)).parameters
    bound = inspect.signature(method).parameters
    ignored = {"update_view"} | (
        {"skip_digestion"} if name == "set_dihedral_angles" else set()
    )
    assert [p for n, p in bound.items() if n not in ignored] == list(native.values())[
        1:
    ]
    assert bound["update_view"].kind is inspect.Parameter.KEYWORD_ONLY
    assert bound["update_view"].default is True and bound["in_place"].default is False
    assert bound["pbc"].default is True
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, name)
    doc = inspect.getdoc(method)
    assert "native in_place=False default" in doc and "No molecular edit" not in doc
    assert "no torsion formula" in doc
    assert "reject nonfinite edit requests" in doc and "explicit block pools" in doc
    assert "Native nonfinite angles can publish NaN" not in doc
    if name == "set_dihedral_angles":
        assert "skip_digestion" not in native
        assert bound["skip_digestion"].kind is inspect.Parameter.KEYWORD_ONLY
        assert "retains ordinary validation" in doc


def test_structure_family_matches_reviewed_public_native_exports(view):
    exports = {
        name
        for name, value in vars(msm.structure).items()
        if not name.startswith("_") and inspect.isfunction(value)
    }
    assert set(dir(view.addons.molsysmt.structure)) == exports
    assert len(exports) == 28


@pytest.mark.parametrize("name", TOOLS)
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("pbc", [False, True])
@pytest.mark.parametrize(
    "length_unit,angle_unit",
    [("nm", "radians"), ("angstrom", "degrees"), ("pm", "degrees")],
)
def test_multiple_torsions_units_repeated_axes_and_native_ownership(
    view, name, in_place, pbc, length_unit, angle_unit
):
    target, state = view.molsys, view.export_state()
    before = xyz(target).copy()
    qs = quartets(target)
    blocks = [blocks_for(target, q) for q in qs]
    values = np.array([[-0.7, 0.4], [0.8, -1.0], [1.1, -0.5]])
    if name == "shift_dihedral_angles":
        values *= 0.3
    expected = before.copy()
    targets = {}
    for row, frame in enumerate(SCOPE):
        desired = values[row].copy()
        if name == "shift_dihedral_angles":
            desired += [torsion(before[frame, q]) for q in qs]
        pose = before[frame].copy()
        for q, block, value in zip(qs, blocks, desired, strict=True):
            pose = rotated(pose, q, block, value)
        expected[frame] = pose
        targets[frame] = desired
    original_analysis = target.interactions["science"]
    box = puw.get_value(msm.get(target, box=True), to_unit="nm").copy()
    argument = puw.convert(puw.quantity(values, "radians"), to_unit=angle_unit)
    with puw.context(standard_units=[length_unit, "ps", angle_unit]):
        result = getattr(view.addons.molsysmt.structure, name)(
            dihedral_quartets=qs,
            structure_indices=SCOPE,
            pbc=pbc,
            in_place=in_place,
            **command(name, argument),
        )
    output = target if in_place else result
    assert result is None if in_place else result is not target
    assert view.molsys is target
    after = xyz(output)
    np.testing.assert_allclose(after, expected, rtol=0, atol=1e-11)
    np.testing.assert_array_equal(after[1], before[1])
    for frame, desired in targets.items():
        observed = np.array([torsion(after[frame, q]) for q in qs])
        np.testing.assert_allclose(
            np.arctan2(np.sin(observed - desired), np.cos(observed - desired)),
            0,
            atol=1e-11,
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
    np.testing.assert_allclose(
        puw.get_value(argument, to_unit="radians"), values, atol=1e-12
    )
    if not in_place:
        np.testing.assert_array_equal(xyz(target), before)
        assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("pbc", [False, True])
@pytest.mark.parametrize("shape", ["scalar", "per_quartet", "per_structure"])
def test_set_native_size_one_broadcast_and_unchanged_box(view, pbc, shape):
    qs = quartets(view.molsys)
    before = xyz(view.molsys).copy()
    values = {
        "scalar": 0.6,
        "per_quartet": [[0.3, -0.7]],
        "per_structure": [[0.2], [0.5], [-0.8]],
    }[shape]
    expected = np.broadcast_to(np.array(values), (3, 2))
    result = view.addons.molsysmt.structure.set_dihedral_angles(
        dihedral_quartets=qs, angles=puw.quantity(values, "radians"), pbc=pbc
    )
    observed = np.array([[torsion(frame[q]) for q in qs] for frame in xyz(result)])
    np.testing.assert_allclose(observed, expected, atol=1e-11)
    np.testing.assert_array_equal(xyz(view.molsys), before)


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("name", TOOLS)
def test_explicit_blocks_move_only_the_requested_atoms(view, in_place, name):
    q = quartets(view.molsys)[0]
    before = xyz(view.molsys).copy()
    moving = {int(q[2]), int(q[3])}
    expected = before.copy()
    target = 0.8 + (torsion(before[2, q]) if name == "shift_dihedral_angles" else 0)
    expected[2] = rotated(before[2], q, moving, target)
    result = getattr(view.addons.molsysmt.structure, name)(
        dihedral_quartets=q,
        **command(name, ".8 radians"),
        blocks=[sorted(moving)],
        structure_indices=[2],
        pbc=False,
        in_place=in_place,
    )
    after = xyz(view.molsys if in_place else result)
    np.testing.assert_allclose(after, expected, rtol=0, atol=1e-11)
    np.testing.assert_array_equal(
        after[:, [i for i in range(before.shape[1]) if i not in moving]],
        before[:, [i for i in range(before.shape[1]) if i not in moving]],
    )


@pytest.mark.parametrize("name", TOOLS)
@pytest.mark.parametrize("triclinic", [False, True])
def test_periodic_rotation_of_a_block_in_another_lattice_image(view, name, triclinic):
    q = quartets(view.molsys)[0]
    block = blocks_for(view.molsys, q)
    box = (
        np.array([[4.0, 0, 0], [0.6, 4, 0], [0.4, 0.2, 4]])
        if triclinic
        else np.eye(3) * 4
    )
    coords = xyz(view.molsys).copy()
    coords[:, sorted(block)] += np.array([1, -1, 1]) @ box
    view.addons.molsysmt.basic.set(
        coordinates=puw.quantity(coords, "nm"),
        box=puw.quantity(np.tile(box, (3, 1, 1)), "nm"),
    )
    angle = 0.7
    target = (
        angle if name == "set_dihedral_angles" else torsion(coords[2, q], box) + angle
    )
    expected = coords.copy()
    expected[2] = rotated(coords[2], q, block, target, box)
    result = getattr(view.addons.molsysmt.structure, name)(
        dihedral_quartets=q,
        structure_indices=[2],
        pbc=True,
        **command(name, puw.quantity(angle, "radians")),
    )
    after = xyz(result)
    np.testing.assert_allclose(after, expected, rtol=0, atol=1e-11)
    np.testing.assert_array_equal(xyz(view.molsys), coords)
    np.testing.assert_allclose(
        np.arctan2(
            np.sin(torsion(after[2, q], box) - target),
            np.cos(torsion(after[2, q], box) - target),
        ),
        0,
        atol=1e-11,
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(result, box=True), to_unit="nm"), np.tile(box, (3, 1, 1))
    )


@pytest.mark.parametrize("name", TOOLS)
def test_native_pbc_true_without_box_falls_back_without_added_preparation(view, name):
    view.addons.molsysmt.basic.set(box=None)
    q = quartets(view.molsys)[0]
    before = xyz(view.molsys).copy()
    desired = 0.5 if name == "set_dihedral_angles" else torsion(before[0, q]) + 0.5
    expected = before.copy()
    expected[0] = rotated(before[0], q, blocks_for(view.molsys, q), desired)
    result = getattr(view.addons.molsysmt.structure, name)(
        dihedral_quartets=q, structure_indices=[0], **command(name, ".5 radians")
    )
    np.testing.assert_allclose(xyz(result), expected, atol=1e-11)
    assert msm.get(result, box=True) is None


@pytest.mark.parametrize("name", TOOLS)
@pytest.mark.parametrize(
    "arguments",
    [
        {"dihedral_quartets": [0, 1, 2]},
        {"invalid_unit": True},
        {"blocks": 1},
        {"blocks": []},
        {"invalid_angle": np.nan},
        {"invalid_angle": np.inf},
        {"invalid_angle": -np.inf},
        {"structure_indices": [-1]},
        {"engine": "unknown"},
    ],
)
def test_native_clean_rejections_keep_geometry_analysis_and_scene(
    view, name, arguments
):
    params = dict(
        dihedral_quartets=quartets(view.molsys)[:1],
        structure_indices=[0],
        pbc=False,
        in_place=True,
    )
    value = (
        puw.quantity(arguments["invalid_angle"], "radians")
        if "invalid_angle" in arguments
        else "1 nm"
        if arguments.get("invalid_unit")
        else ".5 radians"
    )
    params.update(command(name, value))
    params.update(
        {
            n: v
            for n, v in arguments.items()
            if n not in {"invalid_unit", "invalid_angle"}
        }
    )
    before, state, analysis = (
        xyz(view.molsys).copy(),
        view.export_state(),
        view.molsys.interactions["science"],
    )
    with pytest.raises(Exception) as native:
        getattr(msm.structure, name)(msm.copy(view.molsys), **params)
    with pytest.raises(type(native.value)):
        getattr(view.addons.molsysmt.structure, name)(**params)
    np.testing.assert_array_equal(xyz(view.molsys), before)
    assert view.export_state() == state
    assert view.molsys.interactions["science"] is analysis
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("name", TOOLS)
@pytest.mark.parametrize("flags", [{"in_place": "yes"}, {"update_view": 1}])
def test_integration_flags_are_guarded_even_when_digestion_is_skipped(
    view, name, flags
):
    before = xyz(view.molsys).copy()
    with pytest.raises(Exception):
        getattr(view.addons.molsysmt.structure, name)(
            dihedral_quartets=quartets(view.molsys)[:1],
            skip_digestion=True,
            **flags,
            **command(name, puw.quantity([[0.5]], "radians")),
        )
    np.testing.assert_array_equal(xyz(view.molsys), before)


@pytest.mark.parametrize("name", TOOLS)
def test_deferred_torsion_removal_and_translation_retain_scene_maps(view, name):
    tools = view.addons.molsysmt
    q = quartets(view.molsys)[0]
    region = view.regions.add(selection=[14, 24], tag="kept")
    saved = view.selections.add("saved", atom_indices=[14, 24])
    sphere = view.shapes.add_sphere(atom_indices=[24], tag="anchor")
    view.active_selection.set([14, 24])
    view.player.go_to_structure(2)
    source = view.load_blocks[0]["source_id"]
    result = getattr(tools.structure, name)(
        dihedral_quartets=q,
        structure_indices=[2],
        pbc=False,
        in_place=True,
        update_view=False,
        **command(name, ".5 radians"),
    )
    assert result is None
    expected = xyz(view.molsys).copy()
    assert tools.get_sync_status()["state"] == "pending"
    with pytest.raises(SystemEditPendingError):
        region.hide(skip_digestion=True)
    tools.basic.remove(selection=[1], in_place=True, update_view=False)
    expected = np.delete(expected, 1, axis=1)
    tools.structure.translate(
        translation="[0,0,1] nm", in_place=True, update_view=False
    )
    expected += [0, 0, 1]
    storage = view.molsys.structures._coordinates
    tools.sync_view()
    np.testing.assert_allclose(xyz(view.molsys), expected, atol=1e-11)
    assert view.molsys.structures._coordinates is storage
    assert view.regions["kept"] is region and region.atom_indices == (13, 23)
    assert view.selections["saved"] is saved and saved.atom_indices == [13, 23]
    assert view.shapes["anchor"] is sphere
    assert view.active_selection.atom_indices == [13, 23] and view.player.index == 2
    assert view.load_blocks[0]["source_id"] == source
    assert (
        tools.get_sync_status()["target_revision"] == 3 and not view.history.can_undo()
    )


@pytest.mark.parametrize("name", TOOLS)
def test_cached_editor_rebinds_target_and_obeys_lifetime(view, name):
    method = getattr(view.addons.molsysmt.structure, name)
    with msv.demo["dialanine"] as other:
        original, state = xyz(other.molsys).copy(), other.export_state()
        view.load(other.molsys, mode="replace")
        q = quartets(view.molsys)[0]
        result = method(dihedral_quartets=q, pbc=False, **command(name, ".5 radians"))
        assert result is not view.molsys
        np.testing.assert_array_equal(xyz(view.molsys), original)
        np.testing.assert_array_equal(xyz(other.molsys), original)
        assert other.export_state() == state
    with pytest.raises(TypeError):
        method(molecular_system=object(), skip_digestion=True)
    view.close()
    with pytest.raises(RuntimeError, match="closed"):
        method()
    with msv.MolSysView() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.structure, name)()


class InterruptedTorsionWidget(MolSysViewerWidget):
    interrupted = False

    def send(self, content, buffers=None):
        if self.interrupted and content.get("op") == "add_sphere":
            self.interrupted = False
            raise OSError("torsion receiving transport interruption")
        return super().send(content, buffers=buffers)


@pytest.mark.parametrize("name", TOOLS)
def test_sync_retry_does_not_repeat_native_torsion_edit(name):
    with msv.demo["pentalanine"] as source:
        with msv.MolSysView(transport=InterruptedTorsionWidget()) as view:
            view.load(source.molsys, structure_indices=[0, 8, 3])
            q = quartets(view.molsys)[0]
            view.shapes.add_sphere(atom_indices=[14], tag="anchor")
            view._ready = True
            view.widget.interrupted = True
            with pytest.raises(SystemEditSyncError) as error:
                getattr(view.addons.molsysmt.structure, name)(
                    dihedral_quartets=q,
                    structure_indices=[2],
                    pbc=False,
                    in_place=True,
                    **command(name, ".5 radians"),
                )
            assert (
                error.value.science_completed is True
                and error.value.scientific_result is None
            )
            assert isinstance(error.value.__cause__, OSError)
            expected = xyz(view.molsys).copy()
            storage = view.molsys.structures._coordinates
            view.addons.molsysmt.sync_view()
            np.testing.assert_array_equal(xyz(view.molsys), expected)
            assert view.molsys.structures._coordinates is storage
            assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1
