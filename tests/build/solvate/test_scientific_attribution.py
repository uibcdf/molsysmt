"""Retaining each operation's software identity in a shared scientific session."""

import json
import warnings
from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

openmm = pytest.importorskip("openmm")
ackredit = pytest.importorskip("ackredit")
from openmm import app  # noqa: E402

CALLER = "molsysmt.build.solvate"
PAPER = "doi:10.1002/prot.20033"
SOFTWARE_ID = f"software:openmm:{openmm.__version__}"


@pytest.fixture(scope="module")
def solute():
    path = Path(__file__).parents[2] / "form/openmm_Topology/data/obc1_alanine.pdb"
    return msm.convert(app.PDBFile(str(path)))


def _solvate(source):
    return msm.build.solvate(
        source,
        engine="OpenMM",
        box_shape="cubic",
        clearance="0.35 nm",
        n_cations=0,
        n_anions=0,
        random_seed=1,
    )


@pytest.mark.parametrize("order", [("implicit", "solvate"), ("solvate", "implicit")])
@pytest.mark.parametrize("model", ["OBC1", "OBC2"])
def test_alternative_models_share_software_but_keep_separate_uses(solute, order, model):
    atoms = solute.topology.atoms.copy(deep=True)
    groups = solute.topology.groups.copy(deep=True)
    coordinates = solute.structures.coordinates.copy()
    captures, results = {}, {}
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter("always", AckreditTrackingWarning)
        with ackredit.session("alternative-models") as session:
            msm.molecular_mechanics.get_engine_forcefield(
                "AMBER14", implicit_solvent=model
            )
            assert not ackredit.get_used_items()
            with ackredit.capture("both-models") as workflow:
                for operation in order:
                    with ackredit.capture(operation) as run:
                        results[operation] = (
                            _solvate(solute)
                            if operation == "solvate"
                            else msm.convert(
                                solute, to_form="openmm.System", implicit_solvent=model
                            )
                        )
                    captures[operation] = run.attribution.to_dict()
                    assert ackredit.current_session() is session
            enclosing = workflow.attribution.to_dict()
    assert not [
        warning
        for warning in observed
        if issubclass(warning.category, AckreditTrackingWarning)
    ]
    records = []
    for captured in captures.values():
        records.append(
            next(item for item in captured["items"] if item["id"] == SOFTWARE_ID)
        )
        uses = [use for use in captured["uses"] if use["item_id"] == SOFTWARE_ID]
        assert len(uses) == 1
        assert uses[0]["roles"] == ["executed_software"]
    assert records[0] == records[1]
    assert records[0]["title"] == "OpenMM"
    assert records[0]["url"] == "https://openmm.org"
    assert records[0]["version"] == openmm.__version__
    implicit_use = next(
        use for use in captures["implicit"]["uses"] if use["item_id"] == PAPER
    )
    assert implicit_use["context"]["implicit_solvent"] == model
    assert implicit_use["context"]["resources"][-1] == f"implicit/{model.lower()}.xml"
    assert implicit_use["roles"] == ["scientific_criterion"]
    assert PAPER not in {item["id"] for item in captures["solvate"]["items"]}
    solvation_use = next(
        use for use in captures["solvate"]["uses"] if use["item_id"] == SOFTWARE_ID
    )
    assert solvation_use["used_by"] == CALLER
    assert solvation_use["context"]["engine"] == "openmm"
    assert solvation_use["context"]["forcefield"] == [
        "amber14-all.xml",
        "amber14/tip3p.xml",
    ]
    assert solvation_use["context"]["water_model"] == "TIP3P"
    assert solvation_use["context"]["charge_source"] == "not_required"
    assert any(
        use["used_by"] == "molsysmt.build.add_ions"
        for use in captures["solvate"]["uses"]
    )
    assert len([use for use in enclosing["uses"] if use["item_id"] == SOFTWARE_ID]) == 2
    result = results["solvate"]
    stored = result.chemical_states._states[0]._preparation_history[-1]["report"][
        "solvation"
    ]["attribution"]["items"][0]
    assert {key: value for key, value in stored.items() if key != "roles"} == records[0]
    with ackredit.session("reader"):
        restored = ackredit.Attribution.from_dict(
            json.loads(json.dumps(captures["solvate"]))
        )
        assert restored.to_dict() == captures["solvate"]
        assert not ackredit.get_used_items()
    assert result is not solute
    assert result.topology.n_atoms == 151
    assert msm.get(result, n_waters=True) == 43
    assert msm.get(result, n_ions=True) == 0
    assert results["implicit"].getNumParticles() == 22
    assert any(
        isinstance(force, openmm.CustomGBForce)
        for force in results["implicit"].getForces()
    )
    pd.testing.assert_frame_equal(solute.topology.atoms, atoms)
    pd.testing.assert_frame_equal(solute.topology.groups, groups)
    puw = msm.pyunitwizard
    np.testing.assert_array_equal(
        puw.get_value(solute.structures.coordinates), puw.get_value(coordinates)
    )
    shift = (
        puw.get_value(result.structures.coordinates)[0, :22]
        - puw.get_value(coordinates)[0]
    )
    np.testing.assert_allclose(
        shift, np.broadcast_to(shift[0], shift.shape), atol=1e-12
    )


@pytest.mark.parametrize("failure", ["absent", "broken"])
def test_optional_tracking_preserves_solvation_and_detached_provenance(
    solute, monkeypatch, failure
):
    from molsysmt import _ackredit

    with ackredit.session("reference"):
        reference = _solvate(solute)
    expected = deepcopy(
        reference.chemical_states._states[0]._preparation_history[-1]["report"]
    )

    def backend():
        if failure == "broken":
            raise RuntimeError("attribution provider unavailable")
        return None

    monkeypatch.setattr(_ackredit, "backend", backend)
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter("always", AckreditTrackingWarning)
        result = _solvate(solute)
    diagnostics = [
        warning
        for warning in observed
        if issubclass(warning.category, AckreditTrackingWarning)
    ]
    assert bool(diagnostics) == (failure == "broken")
    pd.testing.assert_frame_equal(result.topology.atoms, reference.topology.atoms)
    pd.testing.assert_frame_equal(result.topology.groups, reference.topology.groups)
    puw = msm.pyunitwizard
    np.testing.assert_array_equal(
        puw.get_value(result.structures.coordinates),
        puw.get_value(reference.structures.coordinates),
    )
    report = result.chemical_states._states[0]._preparation_history[-1]["report"]
    np.testing.assert_equal(report, expected)
    assert report is not expected
