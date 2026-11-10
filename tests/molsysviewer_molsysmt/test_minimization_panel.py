"""Reviewed local refinement with native model resolution and retained axes."""

import json
import subprocess

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_geometry_panel import act, mount
from tests.molsysviewer_molsysmt.test_minimization_tools import (
    direct_openmm_minimum,
    same_noncoordinate_domains,
    unchanged_after_rejection,
    xyz,
)
from tests.molsysviewer_molsysmt.test_minimization_tools import engine as engine
from tests.molsysviewer_molsysmt.test_minimization_tools import view as view
from tests.molsysviewer_molsysmt.test_molecular_mechanics_tools import energy_units
from tests.molsysviewer_molsysmt.test_system_panel import transport

puw = msm.pyunitwizard
PARAMETERS = {"task": "minimize", "effect": "result"}


def review(view, **parameters):
    sent = transport(view)
    panel = mount(view)
    packet = act(view, sent, "review", parameters={**PARAMETERS, **parameters})
    return sent, panel, packet


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("platform", ["CPU", "Reference"])
def test_independent_minimum_matches_direct_openmm_and_preserves_source(
    view, engine, unit, platform
):
    before = snapshot(view)
    energy_before, expected_energy, expected_xyz, _ = direct_openmm_minimum(
        view.molsys, engine, platform
    )
    with puw.context(standard_units=[unit, *energy_units("kcal/mol")[1:]]):
        policy = puw.configure.report()
        sent, _, packet = review(view, minimization_platform=platform)
        assert packet["stage"] == "review", packet["message"]
        assert packet["review"]["n_atoms"] == view.molsys.get_n_atoms()
        model = {r["name"]: r for r in packet["review"]["mechanical_model"]}
        assert model["forcefield"]["value"] == "AMBER14"
        assert model["forcefield"]["source"] == "native_default"
        assert model["water_model"]["value"] == "TIP3P"
        assert model["non_bonded_method"]["value"] == "no cutoff"
        assert model["constraints"]["value"] == "hbonds"
        assert model["time_step"]["value"] == pytest.approx(0.001)
        assert model["time_step"]["unit"] == "ps"
        assert model["temperature"]["unit"] == "K"
        unchanged(view, before)
        reviewed_model = packet["review"]["mechanical_model"]
        packet = act(view, sent, "apply", token=packet["review"]["token"])
        assert packet["stage"] == "result", packet["message"]
        child = view.addons.manager.presentations.get(packet["result"]["id"])
        try:
            np.testing.assert_allclose(xyz(child.molsys)[0], expected_xyz, atol=3e-5)
            after = puw.get_value(
                msm.molecular_mechanics.get_potential_energy(
                    child.molsys, platform=platform
                ),
                to_unit="kJ/mol",
            )
            assert after < energy_before
            assert after == pytest.approx(expected_energy, rel=1e-5, abs=0.01)
            same_noncoordinate_domains(child.molsys, view.molsys)
            assert not child.molsys.interactions[
                "science"
            ].evaluated_structure_indices.size
            assert packet["result"]["scientific_parameters"]["model"] == reviewed_model
            assert packet["result"]["scientific_parameters"]["platform"] == platform
            assert len(json.dumps(packet)) < 65536
            unchanged(view, before)
            assert puw.configure.report() == policy
        finally:
            view.addons.manager.presentations.close(packet["result"]["id"])


def test_current_minimum_uses_reviewed_whole_system_and_retains_named_analysis(
    view, engine
):
    target = view.molsys
    source = snapshot(view)
    original = msm.copy(target)
    analysis = target.interactions["science"]
    _, _, expected, _ = direct_openmm_minimum(target, engine)
    sent, _, packet = review(view, effect="update")
    token = packet["review"]["token"]
    packet = act(view, sent, "back")
    unchanged(view, source)
    packet = act(view, sent, "apply", token=token)
    assert packet["stage"] == "error" and "expired" in packet["message"]
    unchanged(view, source)
    packet = act(view, sent, "review", draft={"source": "indices", "indices": "0"})
    assert packet["review"]["n_atoms"] == target.get_n_atoms()
    packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == "done", packet["message"]
    assert (
        view.molsys is target
        and view.addons.molsysmt.get_sync_status()["target_revision"] == 1
    )
    np.testing.assert_allclose(xyz(target)[0], expected, atol=3e-5)
    same_noncoordinate_domains(target, original)
    assert not target.interactions["science"].evaluated_structure_indices.size
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0])
    assert not view.addons.manager.presentations.records()


@pytest.mark.parametrize(
    "field",
    [
        "solute_dielectric",
        "solvent_dielectric",
        "kappa",
        "salt_concentration",
        "cutoff_distance",
    ],
)
def test_unconsumed_stored_controls_are_refused_before_an_edit(view, field):
    setattr(view.molsys.molecular_mechanics, field, 2)
    before = snapshot(view)
    _, _, packet = review(view)
    assert (
        packet["stage"] == "error"
        and "#582" in packet["message"]
        and field in packet["message"]
    )
    assert not packet.get("review") and not view.addons.manager.presentations.records()
    unchanged(view, before)


def test_review_does_not_copy_calculate_or_change_model_and_back_is_noop(
    view, monkeypatch
):
    def forbidden(*args, **kwargs):
        raise AssertionError("Review must not calculate or copy a molecular system")

    before = snapshot(view)
    with monkeypatch.context() as context:
        context.setattr(
            msm.molecular_mechanics, "potential_energy_minimization", forbidden
        )
        context.setattr(msm.basic, "copy", forbidden)
        sent, _, packet = review(view)
    assert packet["stage"] == "review", packet["message"]
    act(view, sent, "back")
    unchanged(view, before)


def test_changed_stored_model_expires_review_before_native_coordinate_work(view):
    sent, _, packet = review(view, effect="update")
    msm.set(view.molsys, forcefield="AMBER99SB")
    before = snapshot(view)
    packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == "error" and "changed" in packet["message"]
    unchanged(view, before)


def test_ensemble_requires_explicit_extraction_without_narrowing_to_visible_structure():
    with (
        msv.demo["pentalanine"] as seed,
        msv.new_view(seed.molsys, structure_indices=[0, 8]) as view,
    ):
        before = snapshot(view)
        _, _, packet = review(view)
        assert (
            packet["stage"] == "error"
            and "Extract one structure explicitly" in packet["message"]
        )
        unchanged(view, before)


def test_bad_forcefield_error_keeps_current_system_unchanged(view, engine):
    # Simulate imported invalid metadata; public setters already reject it.
    view.molsys.molecular_mechanics.forcefield = "not-a-forcefield"
    before = snapshot(view)
    sent, _, packet = review(view, effect="update")
    assert packet["stage"] == "review"
    packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == "error", packet
    unchanged_after_rejection(view, before, True)


def test_refinement_frontend_is_valid_javascript(tmp_path):
    from molsysviewer_molsysmt._geometry_panel_frontend import ESM

    script = tmp_path / "geometry.mjs"
    script.write_text(ESM)
    result = subprocess.run(
        ["node", "--check", str(script)], text=True, capture_output=True
    )
    assert result.returncode == 0, result.stderr
