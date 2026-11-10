"""Receive explicit native repairs/assignments through the real panel authority."""

import json

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    system,
    unchanged,
)
from tests.molsysviewer_molsysmt.test_build_bond_edit_tools import source as bond_source
from tests.molsysviewer_molsysmt.test_build_preparation_tools import source_for
from tests.molsysviewer_molsysmt.test_chemistry_panel import act, mount
from tests.molsysviewer_molsysmt.test_chemistry_preparation_panel import result_view
from tests.molsysviewer_molsysmt.test_system_panel import transport

puw = msm.pyunitwizard
TASKS = (
    "infer_bonds",
    "add_bonds",
    "terminal_cappings",
    "remove_hydrogens",
    "autodock_types",
    "partial_charges",
)


def source(task):
    if task == "infer_bonds":
        return system("infer_covalent_bonds")
    if task == "add_bonds":
        return bond_source()
    if task == "terminal_cappings":
        return source_for("add_missing_terminal_cappings")
    if task == "remove_hydrogens":
        return msm.convert(
            msm.systems["chicken villin HP35"]["1vii.pdb"], to_form="molsysmt.MolSys"
        )
    return system("assign_partial_charges")


def arguments(task):
    return {
        "infer_bonds": (
            "infer_covalent_bonds",
            dict(
                selection="all",
                structure_indices=[0],
                chemical_state="reference",
                method="supported_group_templates",
                return_report=True,
            ),
        ),
        "add_bonds": (
            "add_missing_bonds",
            dict(
                selection="all",
                structure_index=0,
                max_bond_length="2 angstroms",
                engine="MolSysMT",
                in_place=False,
            ),
        ),
        "terminal_cappings": (
            "add_missing_terminal_cappings",
            dict(
                selection="all",
                N_terminal="ACE",
                C_terminal="NME",
                pH=12.0,
                keep_ids=False,
                engine="MolSysMT",
            ),
        ),
        "remove_hydrogens": (
            "reconcile_protonation",
            dict(pH=12.0, engine="MolSysMT", in_place=False),
        ),
        "autodock_types": (
            "assign_autodock_atom_types",
            dict(
                typing_scheme="autodock4",
                method="chemical_environment",
                structure_indices=[0],
                chemical_state="reference",
                return_report=True,
            ),
        ),
        "partial_charges": (
            "assign_partial_charges",
            dict(
                method="gasteiger_marsili",
                structure_indices=[0],
                chemical_state="reference",
                forcefield=None,
                water_model=None,
                expected_total_charge=None,
                return_report=True,
            ),
        ),
    }[task]


@pytest.mark.parametrize("task", TASKS)
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_explicit_native_output_source_preservation_and_bounded_provenance(task, unit):
    with msv.new_view(source(task)) as view:
        view.regions.add(selection=[0], tag="source-region")
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        with puw.context(standard_units=[unit, "ps"]):
            packet = act(
                view,
                sent,
                "prepare",
                draft={"source": "all"},
                parameters={"task": task, "n_cap": "ACE", "c_cap": "NME", "pH": "12"},
            )
            assert packet["stage"] == "prepared", packet["message"]
            child = result_view(view, packet)
            name, kwargs = arguments(task)
            expected = getattr(msm.build, name)(view.molsys, **kwargs)
            same(
                child.molsys,
                expected["molecular_system"]
                if kwargs.get("return_report")
                else expected,
            )
        assert packet["result"]["operation"] == "molsysmt.build." + name
        assert packet["result"]["parameters"]["all_source_structures_retained"]
        assert child.molsys is not view.molsys
        assert (
            child.molsys.structures.n_structures == view.molsys.structures.n_structures
        )
        assert len(json.dumps(packet).encode()) < 65536
        if task == "infer_bonds":
            assert child.molsys.chemical_states.get_bonds()[
                ["atom1_index", "atom2_index"]
            ].values.tolist() == [[0, 1], [0, 5], [1, 2], [1, 4], [2, 3]]
        elif task == "terminal_cappings":
            names = child.molsys.topology.groups.group_name.tolist()
            assert names[0] == "ACE" and names[-1] == "NME"
        elif task == "remove_hydrogens":
            assert child.molsys.get_n_atoms() == view.molsys.get_n_atoms() - 6
        elif task == "autodock_types":
            assert child.molsys.molecular_mechanics.atom_ff_type.tolist() == [
                "C",
                "OA",
                "H",
                "H",
                "H",
                "HD",
            ]
        elif task == "partial_charges":
            np.testing.assert_allclose(
                np.asarray(
                    child.molsys.molecular_mechanics.partial_charge, dtype=float
                ),
                [
                    0.03194068372,
                    -0.39963024356,
                    0.05268663182,
                    0.05268663182,
                    0.05268663182,
                    0.20962966439,
                ],
                rtol=0,
                atol=1e-10,
            )
        unchanged(view, before)
        token = act(view, sent, "replacement.review")["replacement"]["token"]
        act(view, sent, "replacement.back")
        unchanged(view, before)
        expired = act(view, sent, "replacement.apply", token=token)
        assert expired["stage"] == "error"
        unchanged(view, before)


@pytest.mark.parametrize("task", TASKS)
def test_reviewed_replacement_is_explicit_and_separate_result_survives(task):
    with msv.new_view(source(task)) as view:
        view.regions.add(selection=[0], tag="will-reset")
        original = view.molsys
        sent = transport(view)
        mount(view)
        packet = act(
            view,
            sent,
            "prepare",
            draft={"source": "all"},
            parameters={"task": task, "n_cap": "ACE", "c_cap": "NME", "pH": "12"},
        )
        assert packet["stage"] == "prepared", packet["message"]
        child = result_view(view, packet)
        token = act(view, sent, "replacement.review")["replacement"]["token"]
        adopted = act(view, sent, "replacement.apply", token=token)
        assert adopted["stage"] == "prepared", adopted["message"]
        assert adopted["result"]["adopted"] and not adopted["can_replace"]
        assert view.molsys is not original and view.molsys is not child.molsys
        same(view.molsys, child.molsys)
        assert "will-reset" not in view.regions and not child.closed


@pytest.mark.parametrize(
    "task,parameters",
    [
        ("partial_charges", {"expected_charge": "one"}),
        ("partial_charges", {"charge_method": "forcefield", "forcefield": ""}),
        ("partial_charges", {"expected_charge": "9"}),
        ("add_bonds", {"bond_cutoff": "2 ps"}),
        ("terminal_cappings", {"pH": "nan"}),
        ("remove_hydrogens", {"pH": "infinity"}),
        ("infer_bonds", {"inference_method": "guess"}),
    ],
)
def test_errors_have_no_partial_result_source_edit_or_presentation(task, parameters):
    with msv.new_view(source(task)) as view:
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        packet = act(
            view,
            sent,
            "prepare",
            draft={"source": "all"},
            parameters={"task": task, **parameters},
        )
        assert packet["stage"] == "error", packet
        assert not view.addons.manager.presentations.records()
        unchanged(view, before)


@pytest.mark.parametrize(
    "task", ["autodock_types", "partial_charges", "remove_hydrogens"]
)
def test_whole_system_tasks_do_not_use_hidden_atom_or_frame_editor(task):
    with msv.new_view(source(task)) as view:
        sent = transport(view)
        mount(view)
        packet = act(
            view,
            sent,
            "prepare",
            draft={
                "source": "indices",
                "indices": "999999",
                "context": "index",
                "structure_index": 999999,
            },
            parameters={"task": task, "pH": "12"},
        )
        assert packet["stage"] == "prepared", packet["message"]
        assert packet["result"]["parameters"]["scope"] == "whole_system"
        assert packet["result"]["source_atoms"] == view.molsys.get_n_atoms()


@pytest.mark.parametrize("cap", ["NME", "NHE", "NH2"])
def test_explicit_terminal_vocabulary_retains_native_acceptance_or_rejection(cap):
    with msv.new_view(source("terminal_cappings")) as view:
        sent = transport(view)
        mount(view)
        original = snapshot(view)
        try:
            expected = msm.build.add_missing_terminal_cappings(
                view.molsys,
                N_terminal=None,
                C_terminal=cap,
                selection="group_index in [0, 1, 2]",
            )
        except Exception as error:
            packet = act(
                view,
                sent,
                "prepare",
                draft={"source": "all"},
                parameters={"task": "terminal_cappings", "c_cap": cap},
            )
            assert (
                packet["stage"] == "error"
                and not view.addons.manager.presentations.records()
            )
            assert packet["message"] == str(error)[:1000]
        else:
            packet = act(
                view,
                sent,
                "prepare",
                draft={"source": "all"},
                parameters={"task": "terminal_cappings", "c_cap": cap},
            )
            assert packet["stage"] == "prepared", packet["message"]
            same(result_view(view, packet).molsys, expected)
        unchanged(view, original)


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_explicit_forcefield_charge_assignment_matches_independent_ff14sb_values(unit):
    with msv.new_view(
        msm.convert("molsysmt/data/pdb/ala3.pdb", to_form="molsysmt.MolSys")
    ) as view:
        sent = transport(view)
        mount(view)
        original = snapshot(view)
        with puw.context(standard_units=[unit, "fs"]):
            packet = act(
                view,
                sent,
                "prepare",
                parameters={
                    "task": "partial_charges",
                    "charge_method": "forcefield",
                    "forcefield": "AMBER14",
                    "expected_charge": "0",
                },
            )
        assert packet["stage"] == "prepared", packet["message"]
        output = result_view(view, packet).molsys
        values = np.asarray(output.molecular_mechanics.partial_charge, dtype=float)
        actual = {
            row.atom_name: values[i]
            for i, row in view.molsys.topology.atoms.iterrows()
            if row.group_index == 1
        }
        # Published ff14SB internal ALA template, independently of createSystem.
        for name, expected in {
            "N": -0.4157,
            "H": 0.2719,
            "CA": 0.0337,
            "CB": -0.1825,
            "C": 0.5973,
            "O": -0.5679,
        }.items():
            assert actual[name] == pytest.approx(expected)
        assert values.sum() == pytest.approx(0, abs=1e-8)
        assert packet["result"]["parameters"]["forcefield"] == "AMBER14"
        unchanged(view, original)


@pytest.mark.parametrize(
    "field,value", [("charge_method", []), ("inference_method", {}), ("c_cap", None)]
)
def test_malformed_method_fields_are_rejected_before_native_execution(field, value):
    with msv.new_view(source("partial_charges")) as view:
        sent = transport(view)
        mount(view)
        original = snapshot(view)
        packet = act(
            view, sent, "prepare", parameters={"task": "partial_charges", field: value}
        )
        assert packet["stage"] == "error" and "Choose a supported" in packet["message"]
        assert not view.addons.manager.presentations.records()
        unchanged(view, original)
