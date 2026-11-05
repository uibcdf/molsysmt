"""Receive native alternate-site writes and their bounded failure semantics."""

import inspect
import sys
from collections import Counter

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditSyncError
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import same, snapshot
from tests.molsysviewer_molsysmt.test_build_sequence_tools import source as peptide

puw = msm.pyunitwizard
NAME = "solve_atoms_with_alternate_location"


def source():
    result = peptide(multiple=True)
    xyz = puw.get_value(result.structures.coordinates, to_unit="nm")
    count = result.get_n_atoms()
    result.structures.b_factor = puw.quantity(np.full((3, count), 0.1), "nm**2")
    result.structures.occupancy = np.full((3, count), 0.5)
    alternates = []
    for frame in range(3):
        sites = {}
        if frame != 1:
            for atom in (0, 2):
                sites[atom] = {
                    "location_id": np.array(["A", "B"]),
                    "occupancy": np.array([0.5, 0.5]),
                    "atom_id": np.array([f"0{atom}0", f"0{atom}1"]),
                    "coordinates": puw.quantity(
                        [xyz[frame, atom] + 0.01, xyz[frame, atom] + 0.04], "nm"
                    ),
                    "b_factor": puw.quantity([0.12, 0.24], "nm**2"),
                }
        alternates.append(sites)
    result.structures.alternate_location = alternates
    return result


@pytest.fixture
def view():
    with msv.new_view(source()) as view:
        view.regions.add(selection=[0, 2], tag="kept")
        view.shapes.add_sphere(atom_indices=[2], tag="anchor")
        yield view


def structural(actual, expected):
    same(actual, expected)
    for attribute in (
        "b_factor",
        "occupancy",
        "alternate_location",
        "box",
        "time",
        "structure_id",
    ):
        same(
            getattr(actual.structures, attribute),
            getattr(expected.structures, attribute),
        )


def test_signature_help_native_skip_and_expert_namespace(view):
    method = getattr(view.addons.molsysmt.build, NAME)
    native = inspect.signature(getattr(msm.build, NAME))
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
        + [
            inspect.Parameter(
                "update_view", inspect.Parameter.KEYWORD_ONLY, default=True
            ),
        ]
    )
    assert method.digestion_plan is not None and NAME in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, NAME)
    doc = inspect.getdoc(method)
    assert "\nmolecular_system :" not in doc
    for name in inspect.signature(method).parameters:
        assert f"{name} :" in doc
    for name in ("molecular_system", "in_place", "engine", "chemical_state"):
        with pytest.raises(UnknownArgumentError):
            method(**{name: None})


@pytest.mark.parametrize("location", ["A", "B", "occupancy", ["B", "A"]])
@pytest.mark.parametrize("skip", [False, True])
def test_selected_nonconsecutive_sites_keep_native_axes_metadata_and_validity(
    view, location, skip
):
    before = view.molsys.copy()
    expected = before.copy()
    parameters = dict(selection=[2, 0], structure_indices=[2, 0], location_id=location)
    getattr(msm.build, NAME)(expected, **parameters)
    region, sphere = view.regions["kept"], view.shapes["anchor"]
    source_id = view.load_blocks[0]["source_id"]
    assert (
        getattr(view.addons.molsysmt.build, NAME)(**parameters, skip_digestion=skip)
        is None
    )
    structural(view.molsys, expected)
    assert view.molsys.chemical_states._inventory_equals(before.chemical_states)
    assert view.molsys.interactions["saved"].evaluated_structure_indices.tolist() == [1]
    same(
        view.molsys.structures.alternate_location, before.structures.alternate_location
    )
    assert view.regions["kept"] is region and region.atom_indices == (0, 2)
    assert view.shapes["anchor"] is sphere
    assert view.shapes.records()[0]["options"]["atom_indices"] == [2]
    assert view.load_blocks[0]["source_id"] == source_id
    # IDs are topology-wide labels: selected structures must agree. Their
    # labels never replace atom-index scene/source correspondence.
    expected_location = ["A", "B"] if not isinstance(location, str) else [location] * 2
    for atom, chosen in zip((0, 2), expected_location):
        position = 1 if chosen == "B" else 0
        np.testing.assert_allclose(
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[2, atom],
            puw.get_value(
                before.structures.alternate_location[2][atom]["coordinates"],
                to_unit="nm",
            )[position],
        )
        assert msm.get(view.molsys, selection=[atom], atom_id=True) == [
            f"0{atom}{position}"
        ]


@pytest.mark.parametrize(
    "parameters",
    [{"selection": []}, {"structure_indices": []}, {"structure_indices": [1]}],
)
def test_no_site_write_keeps_history_coverage_and_revision(view, parameters):
    view.regions["kept"].hide()
    before = snapshot(view)
    getattr(view.addons.molsysmt.build, NAME)(**parameters, update_view=False)
    structural(view.molsys, before[1])
    assert view.history._undo == before[4][0] and view.history._redo == before[4][1]
    status = view.addons.molsysmt.get_sync_status()
    assert status["state"] == "synchronized" and status["target_revision"] == 0


def test_absent_alternate_metadata_is_native_noop_even_with_local_skip(view):
    view.molsys.structures.alternate_location = None
    before = snapshot(view)
    assert getattr(view.addons.molsysmt.build, NAME)(skip_digestion=True) is None
    structural(view.molsys, before[1])
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


@pytest.mark.parametrize(
    "parameters",
    [
        {"location_id": "not-a-location"},
        {"location_id": "Z"},
        {"selection": [10000]},
        {"structure_indices": [10000]},
    ],
)
def test_clean_native_rejection_preserves_pending_science_and_its_diagnostic(
    view, parameters
):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation="[0,0,1] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        getattr(msm.build, NAME)(view.molsys.copy(), **parameters)
    with pytest.raises(type(native.value)) as actual:
        getattr(tools.build, NAME)(**parameters)
    assert str(actual.value) == str(native.value)
    structural(view.molsys, before[1])
    status = tools.get_sync_status()
    assert status["state"] == "pending" and status["pending_operations"] == 1
    assert status["target_revision"] == before[3]["target_revision"]
    tools.sync_view()


@pytest.mark.parametrize("pending", [False, True])
@pytest.mark.parametrize("skip", [False, True])
def test_late_native_rejection_is_clean_and_preserves_prior_pending_edits(
    view, pending, skip
):
    tools = view.addons.molsysmt
    if pending:
        tools.structure.translate(
            translation="[0,0,1] nm", in_place=True, update_view=False
        )
    view.molsys.structures.alternate_location[2][2]["location_id"] = np.array(
        ["A", "C"]
    )
    before, status = snapshot(view), tools.get_sync_status()
    analysis = view.molsys.interactions["saved"]
    with pytest.raises(Exception) as native:
        getattr(msm.build, NAME)(
            view.molsys.copy(),
            structure_indices=[0, 2],
            location_id="B",
            skip_digestion=skip,
        )
    with pytest.raises(type(native.value)) as actual:
        getattr(tools.build, NAME)(
            structure_indices=[0, 2], location_id="B", skip_digestion=skip
        )
    assert str(actual.value) == str(native.value)
    structural(view.molsys, before[1])
    after_status = tools.get_sync_status()
    assert {k: v for k, v in after_status.items() if k != "operation_id"} == {
        k: v for k, v in status.items() if k != "operation_id"
    }
    assert view.molsys.interactions["saved"] is analysis
    if pending:
        tools.sync_view()
    else:
        view.regions["kept"].hide()


def test_deferred_location_edit_composes_with_removal_and_noop_flushes(view):
    tools = view.addons.molsysmt
    region, sphere = view.regions["kept"], view.shapes["anchor"]
    getattr(tools.build, NAME)(location_id="B", update_view=False)
    assert tools.get_sync_status()["state"] == "pending"
    tools.basic.remove(selection=[1], in_place=True, update_view=False)
    getattr(tools.build, NAME)(structure_indices=[1])  # no sites; project pending work
    assert tools.get_sync_status()["state"] == "synchronized"
    assert tools.get_sync_status()["target_revision"] == 2
    assert view.regions["kept"] is region and region.atom_indices == (0, 1)
    assert view.shapes["anchor"] is sphere
    assert view.shapes.records()[0]["options"]["atom_indices"] == [1]


class InterruptedAlternateWidget(MolSysViewerWidget):
    interrupted = False

    def send(self, content, buffers=None):
        if self.interrupted and content.get("op") == "add_sphere":
            self.interrupted = False
            raise OSError("alternate-site receiving interrupted")
        return super().send(content, buffers=buffers)


def test_projection_retry_never_repeats_native_alternate_resolution():
    with msv.MolSysView(transport=InterruptedAlternateWidget()) as view:
        view.load(source())
        view.shapes.add_sphere(atom_indices=[0], tag="anchor")
        view._ready = True
        view.widget.interrupted = True
        code = inspect.unwrap(getattr(msm.build, NAME)).__code__
        calls = Counter()

        def observe(frame, event, argument):
            if event == "call" and frame.f_code is code:
                calls["native"] += 1

        previous = sys.getprofile()
        sys.setprofile(observe)
        try:
            with pytest.raises(SystemEditSyncError) as error:
                getattr(view.addons.molsysmt.build, NAME)(location_id="B")
            completed = view.molsys.copy()
            view.addons.molsysmt.sync_view()
        finally:
            sys.setprofile(previous)
        assert error.value.science_completed and error.value.scientific_result is None
        assert isinstance(error.value.__cause__, OSError)
        assert calls == {"native": 1}
        structural(view.molsys, completed)


def test_cached_method_uses_replacement_and_rejects_closed_empty_and_flags(view):
    method = getattr(view.addons.molsysmt.build, NAME)
    for parameters in ({"update_view": 1}, {"in_place": True}):
        with pytest.raises(Exception):
            method(skip_digestion=True, **parameters)
    view.load(source(), mode="replace")
    method(location_id="B")
    assert msm.get(view.molsys, selection=[0], atom_id=True) == ["001"]
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.build, NAME)()


def test_bundled_crystallographic_sites_retain_literal_native_coordinates():
    molecular = msm.convert(
        msm.systems["Barnase-Barstar"]["1brs.bcif.gz"], to_form="molsysmt.MolSys"
    )
    with msv.new_view(molecular) as view:
        getattr(view.addons.molsysmt.build, NAME)(location_id="B")
        assert msm.get(view.molsys, selection=[2686, 2687], atom_id=True) == [
            "2688",
            "2690",
        ]
        np.testing.assert_allclose(
            puw.get_value(
                msm.get(view.molsys, selection=[2686, 2687], coordinates=True),
                to_unit="nm",
            ),
            [[[3.2757, 2.2571, 0.1533], [3.3396, 2.192, 0.2619]]],
            rtol=0,
            atol=1e-12,
        )


@pytest.mark.parametrize(
    "length,area", [("nm", "nm**2"), ("angstrom", "angstrom**2"), ("pm", "pm**2")]
)
def test_alternate_quantities_preserve_physical_lengths_and_b_factors(length, area):
    molecular = source()
    for sites in molecular.structures.alternate_location:
        for record in sites.values():
            for name, unit in (("coordinates", length), ("b_factor", area)):
                record[name] = puw.quantity(
                    puw.get_value(record[name], to_unit=unit), unit
                )
    before = molecular.copy()
    with msv.new_view(molecular) as view:
        getattr(view.addons.molsysmt.build, NAME)(location_id="B")
        for frame in (0, 2):
            for atom in (0, 2):
                np.testing.assert_allclose(
                    puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[
                        frame, atom
                    ],
                    puw.get_value(
                        before.structures.alternate_location[frame][atom][
                            "coordinates"
                        ],
                        to_unit="nm",
                    )[1],
                    rtol=0,
                    atol=1e-12,
                )
                assert puw.get_value(view.molsys.structures.b_factor, to_unit="nm**2")[
                    frame, atom
                ] == pytest.approx(0.24)


def test_missing_site_b_factor_becomes_unknown_without_retaining_old_measurement(view):
    view.molsys.structures.alternate_location[0][0]["b_factor"] = None
    expected = view.molsys.copy()
    getattr(msm.build, NAME)(expected, location_id="B")
    getattr(view.addons.molsysmt.build, NAME)(location_id="B")
    structural(view.molsys, expected)
    values = puw.get_value(view.molsys.structures.b_factor, to_unit="nm**2")
    assert np.isnan(values[0, 0])
    assert values[0, 2] == pytest.approx(0.24)
    assert values[1, 0] == pytest.approx(0.1)


@pytest.mark.parametrize(
    "syntax,selection",
    [
        ("MolSysMT", "atom_index in [0, 2]"),
        ("MDTraj", "index 0 or index 2"),
    ],
)
def test_explicit_selection_syntax_reaches_native_resolver(view, syntax, selection):
    expected = view.molsys.copy()
    parameters = dict(selection=selection, syntax=syntax, location_id="B")
    getattr(msm.build, NAME)(expected, **parameters)
    getattr(view.addons.molsysmt.build, NAME)(**parameters)
    structural(view.molsys, expected)


def test_higher_occupancy_choice_and_storage_follow_native_contract(view):
    for sites in view.molsys.structures.alternate_location:
        for record in sites.values():
            record["occupancy"] = np.array([0.4, 0.6])
    expected = view.molsys.copy()
    getattr(msm.build, NAME)(expected)
    getattr(view.addons.molsysmt.build, NAME)()
    structural(view.molsys, expected)
    assert msm.get(view.molsys, selection=[0], atom_id=True) == ["001"]


def test_forwarded_skip_does_not_disable_native_site_validation(view):
    before = view.molsys.copy()
    with pytest.raises(Exception) as native:
        getattr(msm.build, NAME)(
            before, location_id="not-a-location", skip_digestion=True
        )
    with pytest.raises(type(native.value)) as actual:
        getattr(view.addons.molsysmt.build, NAME)(
            location_id="not-a-location", skip_digestion=True
        )
    assert str(actual.value) == str(native.value)
    structural(view.molsys, before)


@pytest.mark.parametrize(
    "occupancies,position", [([0.2, 0.5], 1), ([0.4, 0.6], 1), ([0.5, 0.5], 0)]
)
@pytest.mark.parametrize("skip", [False, True])
def test_chosen_primary_measurements_match_literal_alternate_observations(
    view, occupancies, position, skip
):
    for frame in (0, 2):
        view.molsys.structures.alternate_location[frame][0]["occupancy"] = np.array(
            occupancies
        )
    selected = view.molsys.structures.alternate_location[2][0]
    xyz = puw.get_value(selected["coordinates"], to_unit="nm")[position].copy()
    getattr(view.addons.molsysmt.build, NAME)(
        selection=[0], structure_indices=[2, 0], skip_digestion=skip
    )
    for frame in (0, 2):
        assert view.molsys.structures.occupancy[frame, 0] == pytest.approx(
            occupancies[position]
        )
        assert puw.get_value(view.molsys.structures.b_factor, to_unit="nm**2")[
            frame, 0
        ] == pytest.approx([0.12, 0.24][position])
    np.testing.assert_allclose(
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[2, 0], xyz
    )
    assert msm.get(view.molsys, selection=[0], element="atom", atom_id=True) == [
        f"00{position}"
    ]
    assert view.molsys.structures.occupancy[1, 0] == pytest.approx(0.5)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1


def test_conflicting_stable_labels_are_rejected_without_source_or_scene_edits(view):
    view.molsys.structures.alternate_location[2][0]["atom_id"][1] = "conflict"
    before = snapshot(view)
    analysis = view.molsys.interactions["saved"]
    with pytest.raises(Exception) as native:
        getattr(msm.build, NAME)(view.molsys.copy(), location_id="B")
    with pytest.raises(type(native.value)) as actual:
        getattr(view.addons.molsysmt.build, NAME)(location_id="B")
    assert str(actual.value) == str(native.value)
    structural(view.molsys, before[1])
    assert view.molsys.interactions["saved"] is analysis
    assert view.export_state() == before[2]
    assert view.history._undo == before[4][0] and view.history._redo == before[4][1]
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
