"""Receiving real geometry writes without losing unedited analysis coverage."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError as NativeArgumentError

system_edits = pytest.importorskip("molsysviewer.system_edits")
puw = msm.pyunitwizard


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            msm.set(
                result.molsys, box=puw.quantity(np.tile(np.eye(3) * 3, (3, 1, 1)), "nm")
            )
            analysis = msm.Interactions.from_records(
                [
                    {
                        "structure_index": frame,
                        "interaction_type": "hbond",
                        "participants": [
                            {"role": role, "atom_indices": [atom]}
                            for atom, role in enumerate(
                                ("donor", "hydrogen", "acceptor")
                            )
                        ],
                    }
                    for frame in range(3)
                ],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.geometry",
            )
            result.interactions.attach(analysis, name="first", assume_aligned=True)
            result.interactions.attach(
                analysis.remap(), name="second", assume_aligned=True
            )
            result.interactions.add("first", tag="hb")
            yield result


def _values(quantity):
    return None if quantity is None else puw.get_value(quantity, to_unit="nm")


def test_signature_matches_native_plus_explicit_keyword_control(view):
    native = list(inspect.signature(msm.basic.set).parameters.values())[1:]
    bound = inspect.signature(view.addons.molsysmt.basic.set)
    assert [
        value for name, value in bound.parameters.items() if name != "update_view"
    ] == native
    assert bound.parameters["update_view"].kind is inspect.Parameter.KEYWORD_ONLY
    assert bound.parameters["update_view"].default is True
    assert getattr(view.addons.molsysmt.basic.set, "digestion_plan", None) is not None
    assert view.addons.molsysmt.set == view.addons.molsysmt.basic.set
    assert "coordinates and box" in inspect.getdoc(view.addons.molsysmt.basic.set)


@pytest.mark.parametrize("frames", [[2, 0], [2, 0, 2], [1], "all"])
@pytest.mark.parametrize("attribute", ["coordinates", "box"])
def test_native_units_order_duplicate_writes_and_exact_invalidation(
    view, frames, attribute
):
    target = view.molsys
    originals = dict(target.interactions)
    native = msm.copy(target)
    frame_list = list(range(3)) if frames == "all" else frames
    selection = [2, 0] if attribute == "coordinates" else "all"
    shape = (len(frame_list), 2 if attribute == "coordinates" else 3, 3)
    values = np.arange(np.prod(shape), dtype=float).reshape(shape) + 10
    if attribute == "box":
        values = np.array([np.diag([20 + frame, 30, 40]) for frame in frame_list])
    parameters = dict(
        selection=selection,
        structure_indices=frames,
        **{attribute: puw.quantity(values, "angstrom")},
    )
    expected = msm.basic.set(native, **parameters)
    result = view.addons.molsysmt.basic.set(**parameters)
    assert result is expected is None
    assert view.molsys is target
    np.testing.assert_array_equal(
        _values(target.structures.coordinates), _values(native.structures.coordinates)
    )
    np.testing.assert_array_equal(
        _values(target.structures.box), _values(native.structures.box)
    )
    for name, original in originals.items():
        np.testing.assert_array_equal(original.evaluated_structure_indices, [0, 1, 2])
        np.testing.assert_array_equal(
            target.interactions[name].evaluated_structure_indices,
            [frame for frame in range(3) if frame not in frame_list],
        )
        assert target.interactions[name].method == original.method
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
    assert not view.history.can_undo()


def test_deferred_geometry_and_removal_compose_without_repeating_science(view):
    tools = view.addons.molsysmt
    region = view.regions.add(atom_indices=[2, 3], tag="kept")
    tools.remove(selection=[0], in_place=True, update_view=False)
    xyz = tools.get(
        element="atom", selection=[1], structure_indices=[2, 0], coordinates=True
    )
    tools.set(
        selection=[1],
        structure_indices=[2, 0],
        coordinates=xyz + puw.quantity(0.2, "nm"),
        update_view=False,
    )
    new_xyz = _values(view.molsys.structures.coordinates).copy()
    assert tools.get_sync_status()["pending_operations"] == 2
    assert tools.get_sync_status()["state"] == "pending"
    tools.sync_view()
    assert view.regions["kept"] is region and region.atom_indices == (1, 2)
    np.testing.assert_array_equal(_values(view.molsys.structures.coordinates), new_xyz)
    np.testing.assert_array_equal(
        view.molsys.interactions["second"].evaluated_structure_indices, [1]
    )


def test_combined_geometry_values_are_validated_before_any_native_write(view):
    target = view.molsys
    coordinates = _values(target.structures.coordinates).copy()
    analyses = dict(target.interactions)
    with pytest.raises(NativeArgumentError):
        view.addons.molsysmt.set(
            structure_indices=[0],
            selection=[0],
            coordinates=puw.quantity([[[0, 0, 0]]], "nm"),
            box=puw.quantity(np.ones((1, 2, 2)), "nm"),
        )
    np.testing.assert_array_equal(_values(target.structures.coordinates), coordinates)
    assert all(target.interactions[name] is value for name, value in analyses.items())
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize(
    "attributes",
    [
        {"group_name": "X"},
        {"coordinates": None},
        {"box": puw.quantity(np.eye(3), "nm")},
        {"coordinates": puw.quantity(np.ones((1, 2, 3)), "ps")},
    ],
)
def test_unreceived_effects_shape_and_units_reject_without_blocking(view, attributes):
    before = view.export_state()
    analyses = dict(view.molsys.interactions)
    with pytest.raises((NativeArgumentError, ValueError, NotImplementedError)):
        view.addons.molsysmt.set(**attributes)
    assert view.export_state() == before
    assert all(
        view.molsys.interactions[name] is result for name, result in analyses.items()
    )
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


def test_box_clear_and_partial_missing_box_initialization(view):
    tools = view.addons.molsysmt
    assert tools.set(box=None) is None
    assert view.molsys.structures.box is None
    with pytest.raises(ValueError, match="full box series"):
        tools.set(
            structure_indices=[2, 0],
            box=puw.quantity(np.tile(np.eye(3), (2, 1, 1)), "nm"),
        )
    assert tools.get_sync_status()["state"] == "synchronized"
    tools.set(box=puw.quantity(np.tile(np.eye(3) * 4, (3, 1, 1)), "nm"))
    assert _values(view.molsys.structures.box).shape == (3, 3, 3)


def test_noop_and_empty_atom_selection_preserve_revision_and_coverage(view):
    tools = view.addons.molsysmt
    analyses = dict(view.molsys.interactions)
    tools.set()
    tools.set(selection=[], coordinates=puw.quantity(np.empty((3, 0, 3)), "nm"))
    assert tools.get_sync_status()["target_revision"] == 0
    assert all(
        view.molsys.interactions[name] is result for name, result in analyses.items()
    )


def test_postpublication_exception_is_uncertain_even_without_molsys_dictionary_replacement(
    view,
):
    from molsysviewer_molsysmt._geometry import _geometry_token, _prepare_geometry_set

    target = view.molsys
    before = vars(target)
    coordinates = puw.quantity(np.ones((1, 1, 3)), "nm")

    def prepare(system):
        plan = _prepare_geometry_set(
            system,
            dict(
                element=None,
                selection=[0],
                structure_indices=[0],
                syntax="MolSysMT",
                chemical_state="reference",
                skip_digestion=False,
            ),
            {"coordinates": coordinates},
        )
        native_run = plan["run"]

        def run():
            native_run()
            raise RuntimeError("receiving interruption after real geometry publication")

        plan["run"] = run
        return plan

    with pytest.raises(RuntimeError, match="real geometry publication"):
        view.addons.manager.system_edits.execute(
            prepare,
            name="receiving.geometry_interruption",
            rejection_check=_geometry_token,
        )
    assert vars(target) is before
    np.testing.assert_array_equal(
        _values(target.structures.coordinates)[0, 0], [1, 1, 1]
    )
    assert view.addons.molsysmt.get_sync_status()["state"] == "uncertain"
    with pytest.raises(system_edits.SystemEditPendingError):
        view.addons.molsysmt.sync_view()


def test_pending_rejection_keeps_prior_changes_and_synchronization_maps(view):
    tools = view.addons.molsysmt
    tools.remove(selection=[0], in_place=True, update_view=False)
    coordinates = _values(view.molsys.structures.coordinates).copy()
    status = tools.get_sync_status()
    with pytest.raises(ValueError, match="selected structure"):
        tools.set(
            structure_indices=[2, 0], coordinates=puw.quantity(coordinates[:1], "nm")
        )
    assert tools.get_sync_status() == status
    np.testing.assert_array_equal(
        _values(view.molsys.structures.coordinates), coordinates
    )
    tools.sync_view()


def test_cached_setter_follows_replacement_and_closed_view_guard(view):
    setter = view.addons.molsysmt.basic.set
    with msv.demo["dialanine"] as source:
        view.load(source.molsys, mode="replace")
    coordinates = msm.get(view.molsys, element="atom", coordinates=True).copy()
    assert setter(coordinates=coordinates + puw.quantity(0.1, "nm")) is None
    view.close()
    with pytest.raises(RuntimeError, match="closed"):
        setter(coordinates=coordinates)


def test_keyword_typo_uses_native_attribute_domain_before_effect_receiving(view):
    from argdigest import UnknownArgumentError

    state = view.addons.molsysmt.get_sync_status()
    with pytest.raises(UnknownArgumentError):
        view.addons.molsysmt.set(coordnates=puw.quantity(np.ones((3, 62, 3)), "nm"))
    assert view.addons.molsysmt.get_sync_status() == state


def test_real_buch_results_keep_unedited_structure_and_old_snapshot(view):
    analysis = msm.interactions.hbonds.get_buch_hbonds(
        view.molsys,
        structure_indices="all",
        pbc=False,
        output_type="molsysmt.Interactions",
    )
    view.interactions.attach(analysis, name="calculated", assume_aligned=True)
    before = analysis.query(structure_indices=[1]).to_dict()
    coordinates = view.addons.molsysmt.get(
        element="atom", structure_indices=[2, 0], coordinates=True
    )
    view.addons.molsysmt.set(
        structure_indices=[2, 0], coordinates=coordinates + puw.quantity(0.1, "nm")
    )
    updated = view.molsys.interactions["calculated"]
    np.testing.assert_array_equal(updated.evaluated_structure_indices, [1])
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1, 2])
    after = updated.query(structure_indices=[1]).to_dict()
    np.testing.assert_array_equal(
        after["occurrence_indices"], before["occurrence_indices"]
    )
    assert updated.method == analysis.method
    assert updated.parameters == analysis.parameters
    assert updated.measure_units == analysis.measure_units


def test_projection_retry_preserves_geometry_storage_and_unedited_coverage():
    from molsysviewer.widget import MolSysViewerWidget

    class InterruptedWidget(MolSysViewerWidget):
        interrupted = False

        def send(self, content, buffers=None):
            if self.interrupted and content.get("op") == "add_sphere":
                self.interrupted = False
                raise OSError("receiving connector interruption")
            return super().send(content, buffers=buffers)

    with msv.demo["pentalanine"] as source:
        with msv.MolSysView(transport=InterruptedWidget()) as view:
            view.load(source.molsys, structure_indices=[0, 8, 3])
            analysis = msm.interactions.hbonds.get_buch_hbonds(
                view.molsys,
                pbc=False,
                structure_indices="all",
                output_type="molsysmt.Interactions",
            )
            view.interactions.attach(analysis, name="calculated", assume_aligned=True)
            view.shapes.add_sphere(atom_indices=[0], tag="anchor")
            view._ready = True
            view.widget.interrupted = True
            coordinates = msm.get(
                view.molsys, element="atom", structure_indices=[0], coordinates=True
            )
            with pytest.raises(system_edits.SystemEditSyncError) as error:
                view.addons.molsysmt.set(
                    structure_indices=[0],
                    coordinates=coordinates + puw.quantity(0.1, "nm"),
                )
            assert (
                error.value.science_completed and error.value.scientific_result is None
            )
            assert isinstance(error.value.__cause__, OSError)
            storage = view.molsys.structures._coordinates
            updated = view.molsys.interactions["calculated"]
            assert view.addons.molsysmt.get_sync_status()["state"] == "sync_failed"
            view.addons.molsysmt.sync_view()
            assert view.molsys.structures._coordinates is storage
            assert view.molsys.interactions["calculated"] is updated
            np.testing.assert_array_equal(updated.evaluated_structure_indices, [1, 2])
            assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1
