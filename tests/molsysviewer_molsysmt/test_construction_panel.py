"""Receive native construction without implicit adoption or hidden preparation."""

import json

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from tests.build.make_bioassembly.test_structure_selection import molsys as assembly
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_chemistry_panel import act, mount
from tests.molsysviewer_molsysmt.test_chemistry_preparation_panel import result_view
from tests.molsysviewer_molsysmt.test_solvation_tools import source
from tests.molsysviewer_molsysmt.test_system_panel import transport

puw = msm.pyunitwizard
__all__ = ["assembly"]


def check_result(view, packet):
    assert packet["stage"] == "prepared", packet["message"]
    assert packet["can_replace"]
    assert len(json.dumps(packet).encode()) < 65536
    child = result_view(view, packet)
    assert child.molsys is not view.molsys
    return child


def close_results(view):
    for row in view.addons.manager.presentations.records():
        view.addons.manager.presentations.close(row["id"])


def test_explicit_peptide_starts_empty_and_replacement_is_deliberate():
    with msv.new_view() as view:
        sent = transport(view)
        mount(view)
        packet = act(
            view, sent, "prepare", parameters={"task": "peptide", "sequence": "AlaGly"}
        )
        child = check_result(view, packet)
        assert view.molsys is None
        expected = msm.build.build_peptide(
            "amino_acids_3:AlaGly", from_naming_scheme="sequence"
        )
        np.testing.assert_array_equal(
            puw.get_value(child.molsys.structures.coordinates, to_unit="nm"),
            puw.get_value(expected.structures.coordinates, to_unit="nm"),
        )
        packet = act(view, sent, "replacement.review")
        assert packet["replacement"]
        packet = act(view, sent, "replacement.back")
        assert view.molsys is None and not packet["replacement"]
        packet = act(view, sent, "replacement.review")
        packet = act(
            view, sent, "replacement.apply", token=packet["replacement"]["token"]
        )
        assert packet["stage"] == "prepared", packet["message"]
        assert (
            view.molsys is not child.molsys
            and view.molsys.get_n_atoms() == expected.get_n_atoms()
        )
        child.addons.molsysmt.structure.translate(
            translation="[1,0,0] nm", in_place=True
        )
        np.testing.assert_array_equal(
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm"),
            puw.get_value(expected.structures.coordinates, to_unit="nm"),
        )
        close_results(view)


@pytest.mark.parametrize("unit,edge", [("nm", "2"), ("angstrom", "20"), ("pm", "2000")])
def test_water_cell_starts_empty_with_explicit_typed_cell(unit, edge):
    with msv.new_view() as view:
        sent = transport(view)
        mount(view)
        packet = act(
            view,
            sent,
            "prepare",
            parameters={
                "task": "water_cell",
                "cell_a": edge,
                "cell_b": edge,
                "cell_c": edge,
                "cell_length_unit": unit,
            },
        )
        child = check_result(view, packet)
        assert view.molsys is None
        assert msm.get(child.molsys, n_waters=True) == 268
        np.testing.assert_allclose(
            puw.get_value(child.molsys.structures.box, to_unit="nm"),
            [2 * np.eye(3)],
            atol=1e-14,
        )
        assert packet["result"]["parameters"]["box_unit"] == "nm"
        assert "no parameter" in packet["result"]["parameters"]["reference"]
        assert child.molsys.molecular_mechanics.forcefield is None
        close_results(view)


def test_fresh_input_does_not_edit_loaded_source_or_follow_its_selection():
    with msv.demo["pentalanine"] as view:
        view.active_selection.set([0])
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        packet = act(
            view,
            sent,
            "prepare",
            draft={"source": "indices", "indices": "999999"},
            parameters={
                "task": "peptide",
                "sequence": "AG",
                "sequence_format": "amino_acids_1",
            },
        )
        child = check_result(view, packet)
        assert child.molsys.get_n_atoms() != view.molsys.get_n_atoms()
        unchanged(view, before)
        packet = act(view, sent, "replacement.review")
        token = packet["replacement"]["token"]
        view.addons.molsysmt.structure.translate(
            translation="[0.1,0,0] nm", in_place=True
        )
        packet = act(view, sent, "replacement.apply", token=token)
        assert packet["stage"] == "error" and not packet["can_replace"]
        assert packet["result"]
        close_results(view)


def test_named_assembly_retains_nonconsecutive_repeated_structures(assembly):
    with msv.new_view(assembly) as view:
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        packet = act(
            view,
            sent,
            "prepare",
            parameters={
                "task": "bioassembly",
                "assembly_name": "1",
                "construction_structures": "indices",
                "construction_indices": "2,0,2",
            },
        )
        child = check_result(view, packet)
        expected = msm.build.make_bioassembly(
            view.molsys, bioassembly="1", structure_indices=[2, 0, 2]
        )
        assert child.molsys.structures.structure_id.tolist() == [
            "label-C",
            "label-A",
            "label-C",
        ]
        np.testing.assert_allclose(
            puw.get_value(child.molsys.structures.coordinates, to_unit="nm"),
            puw.get_value(expected.structures.coordinates, to_unit="nm"),
            rtol=0,
            atol=1e-13,
        )
        assert packet["result"]["structure_indices"] == [2, 0, 2]
        unchanged(view, before)
        close_results(view)


def test_solvent_and_explicit_requests_remain_independent():
    with msv.new_view(source()) as view:
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        parameters = {
            "task": "solvate",
            "clearance": "0.35 nm",
            "construction_forcefield": "AMBER14",
            "random_seed": "19",
        }
        packet = act(view, sent, "prepare", parameters=parameters)
        child = check_result(view, packet)
        assert msm.get(child.molsys, n_waters=True) > 0
        assert child.molsys.structures.n_structures == 1
        assert packet["result"]["parameters"]["random_seed"] == 19
        assert packet["result"]["parameters"]["declared_requests"] == {
            "water_model": "TIP3P",
            "forcefield": "AMBER14",
        }
        unchanged(view, before)
        close_results(view)


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_ion_counts_native_seed_and_full_report_survive_in_result(unit):
    water = msm.build.make_water_box(puw.quantity(2 * np.eye(3), "nm"))
    with msv.new_view(water) as view:
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        parameters = {
            "task": "ions",
            "n_cations": "2",
            "n_anions": "1",
            "random_seed": "19",
        }
        with puw.context(standard_units=[unit, "ps"]):
            packet = act(view, sent, "prepare", parameters=parameters)
            expected = msm.build.add_ions(
                view.molsys, n_cations=2, n_anions=1, random_seed=19, return_report=True
            )
        child = check_result(view, packet)
        assert msm.get(child.molsys, n_ions=True, n_waters=True) == [3, 265]
        np.testing.assert_array_equal(
            puw.get_value(child.molsys.structures.coordinates, to_unit="nm"),
            puw.get_value(
                expected["molecular_system"].structures.coordinates, to_unit="nm"
            ),
        )
        assert (
            packet["result"]["parameters"]["report_schema"]
            == expected["report"]["schema"]
        )
        assert "output_to_source_atom_indices" not in json.dumps(packet)
        envelope = next(
            row
            for row in reversed(child.molsys.chemical_states.get_preparation_history())
            if row["report"]["schema"] == expected["report"]["schema"]
        )
        assert envelope["index_scope"] == "operation"
        assert envelope["output"]["n_atoms"] == child.molsys.get_n_atoms()
        stored = envelope["report"]
        for name in ("random", "requested", "added", "parameters", "software"):
            assert stored[name] == expected["report"][name]
        for name in (
            "output_to_source_atom_indices",
            "source_to_output_atom_indices",
            "removed_atom_indices",
        ):
            np.testing.assert_array_equal(stored[name], expected["report"][name])
        stored["output_to_source_atom_indices"][0] = -999
        retained = next(
            row["report"]
            for row in reversed(child.molsys.chemical_states.get_preparation_history())
            if row["report"]["schema"] == expected["report"]["schema"]
        )
        np.testing.assert_array_equal(
            retained["output_to_source_atom_indices"],
            expected["report"]["output_to_source_atom_indices"],
        )
        unchanged(view, before)
        close_results(view)


@pytest.mark.parametrize(
    "parameters",
    [
        {"task": "peptide", "sequence": ""},
        {"task": "peptide", "sequence": "AG", "naming_scheme": "invented"},
        {"task": "water_cell", "cell_a": "nan"},
        {"task": "water_cell", "cell_alpha": "0"},
        {"task": "bioassembly", "assembly_name": "missing"},
        {"task": "solvate", "random_seed": "-1"},
        {"task": "ions", "n_anions": "1.5"},
        {"task": "ions", "charge_source": "selected_fragment"},
    ],
)
def test_invalid_construction_has_no_partial_result_or_source_edit(parameters):
    with msv.demo["pentalanine"] as view:
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        packet = act(view, sent, "prepare", parameters=parameters)
        assert packet["stage"] == "error", packet["message"]
        assert not packet["result"] and not view.addons.manager.presentations.records()
        unchanged(view, before)


@pytest.mark.parametrize("task", ["solvate", "ions"])
def test_source_construction_refuses_trajectory_loop_before_native_calculation(task):
    with msv.demo["pentalanine"] as view:
        # The bundled trajectory is explicit, not duplicated from a singleton.
        view.load(msm.systems["pentalanine"]["traj_pentalanine.h5msm"], mode="replace")
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        packet = act(
            view,
            sent,
            "prepare",
            parameters={
                "task": task,
                "construction_structures": "indices",
                "construction_indices": "2,0",
            },
        )
        assert packet["stage"] == "error" and "exactly one" in packet["message"]
        assert not packet["result"]
        unchanged(view, before)
