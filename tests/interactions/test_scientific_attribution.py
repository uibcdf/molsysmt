"""Protect criterion naming, real Ackredit use and portable result bibliography."""

import json
import subprocess
import sys
from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from tests.interactions.cation_pi.test_get_cation_pi_interactions import (
    _system as cation_system,
)
from tests.interactions.hbonds.test_attributed_hbonds import _system as hbond_system


def _assert_observations_equal(first, second):
    for name in (
        "participant_atoms",
        "participant_atom_offsets",
        "occurrence_structures",
        "occurrence_relations",
        "evaluated_structure_indices",
        "image_vectors",
    ):
        np.testing.assert_array_equal(getattr(first, name), getattr(second, name))
    assert first.participant_roles == second.participant_roles
    assert first.parameters == second.parameters
    for name in first.measurements:
        np.testing.assert_array_equal(
            first.measurements[name], second.measurements[name]
        )


@pytest.mark.parametrize(
    "alias,method,profile",
    [
        ("cpptraj", "donor_acceptor_distance_angle", "elemental_fon"),
        ("prolif", "donor_acceptor_distance_angle", "smarts_donor_acceptor"),
        ("mdanalysis_geometry", "donor_acceptor_distance_angle", "explicit_sites"),
    ],
)
def test_hbond_canonical_profiles_preserve_exact_legacy_observations(
    alias, method, profile
):
    molsys = hbond_system()
    options = dict(pbc=False, structure_indices=[2, 0, 2])
    if profile == "explicit_sites":
        options.update(donor_hydrogen_pairs=[[0, 2]], acceptor_atom_indices=[1])
    old = msm.interactions.hbonds.get_hbonds(molsys, method=alias, **options)
    new = msm.interactions.hbonds.get_hbonds(
        molsys, method=method, profile=profile, **options
    )
    _assert_observations_equal(old, new)
    assert new.parameters["method"] == method
    assert new.parameters["profile"] == profile


@pytest.mark.parametrize(
    "alias,method,profile",
    [
        ("prolif", "centroid_distance_angle", "smarts_5_6"),
        ("molstar_geometry", "centroid_distance_offset", "three_atom_plane"),
    ],
)
def test_cation_profiles_and_default_preserve_legacy_geometry(alias, method, profile):
    molsys = cation_system()
    old = msm.interactions.cation_pi.get_cation_pi_interactions(
        molsys, method=alias, pbc=False
    )
    new = msm.interactions.cation_pi.get_cation_pi_interactions(
        molsys, method=method, profile=profile, pbc=False
    )
    _assert_observations_equal(old, new)
    if alias == "prolif":
        _assert_observations_equal(
            old,
            msm.interactions.cation_pi.get_cation_pi_interactions(molsys, pbc=False),
        )


def test_profiles_refuse_ambiguous_or_invalid_combinations():
    molsys = hbond_system()
    for method, profile in [
        ("prolif", "elemental_fon"),
        ("baker_hubbard", "explicit_sites"),
        ("donor_acceptor_distance_angle", "unknown"),
    ]:
        with pytest.raises(msm.ArgumentError):
            msm.interactions.hbonds.get_hbonds(molsys, method=method, profile=profile)


@pytest.mark.parametrize(
    "alias,method,profile",
    [
        ("prolif", "plane_angle_intersection", "smarts_5_6"),
        ("mdtraj_geometry", "plane_angle_intersection", "aromatic_cycles"),
        ("molstar_geometry", "centroid_angle_offset", "three_atom_plane"),
    ],
)
def test_pi_pi_canonical_profiles_preserve_legacy_observations(alias, method, profile):
    from rdkit import Chem

    phase = np.arange(6) * np.pi / 3
    ring = 0.14 * np.column_stack((np.cos(phase), np.sin(phase), np.zeros(6)))
    molsys = msm.convert(
        Chem.MolFromSmiles("c1ccccc1.c1ccccc1"), to_form="molsysmt.MolSys"
    )
    molsys.structures.append(
        coordinates=msm.pyunitwizard.quantity(
            [np.concatenate((ring, ring + [0, 0, 0.35]))], "nm"
        )
    )
    old = msm.interactions.pi_pi.get_pi_pi_interactions(molsys, method=alias, pbc=False)
    new = msm.interactions.pi_pi.get_pi_pi_interactions(
        molsys, method=method, profile=profile, pbc=False
    )
    assert new.n_interactions == 1
    _assert_observations_equal(old, new)


def test_real_ackredit_exact_references_reused_results_empty_frames_and_enclosing_scope():
    ackredit = pytest.importorskip("ackredit")
    molsys = hbond_system()
    paper = "doi:10.1016/0079-6107(84)90007-5"
    unrelated = "doi:10.1186/s13321-021-00548-6"
    with ackredit.session("viewer-test"):
        with ackredit.scope("molsysviewer.interactions.calculate"):
            first = msm.interactions.hbonds.get_hbonds(
                molsys, pbc=False, structure_indices=[2, 0, 2]
            )
            empty = msm.interactions.hbonds.get_hbonds(
                molsys, pbc=False, structure_indices=[1]
            )
        assert empty.n_interactions == 0
        assert empty.evaluated_structure_indices.tolist() == [1]
        for result in (first, empty):
            items = result.parameters["attribution"]["items"]
            by_id = {item["id"]: item for item in items}
            assert by_id[paper]["roles"] == ["scientific_criterion"]
            assert by_id[paper]["authors"] == ["Baker, E. N.", "Hubbard, R. E."]
            assert unrelated not in by_id
            assert not any(
                item.get("type") == "software" and item["title"] == "MDTraj"
                for item in items
            )
        used = ackredit.get_used_items()
        assert paper in used and unrelated not in used
        assert len(used[paper]) == 1
        report = json.loads(ackredit.report(format="json"))
        assert next(item for item in report if item["id"] == paper)["doi"] == paper[4:]
        tree = ackredit.current_session().usage_tree
        assert (
            "molsysmt.interactions.hbonds.get_hbonds"
            in tree["molsysviewer.interactions.calculate"]["children"]
        )


def test_smarts_branch_credits_reference_and_only_executed_dependencies():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("smarts-test"):
        result = msm.interactions.cation_pi.get_cation_pi_interactions(
            cation_system(), pbc=False
        )
        items = result.parameters["attribution"]["items"]
        reference = next(
            item for item in items if item.get("doi") == "10.1186/s13321-021-00548-6"
        )
        assert reference["roles"] == ["reference_implementation"]
        assert "rdkit" in result.software
        assert any(item["id"].startswith("software:rdkit:") for item in items)
        assert not any(item["id"].startswith("software:prolif:") for item in items)
        assert reference["id"] in ackredit.get_used_items()


def test_result_bibliography_is_detached_from_registry_and_other_results():
    ackredit = pytest.importorskip("ackredit")
    paper = "doi:10.1016/0079-6107(84)90007-5"
    with ackredit.session("detached-test"):
        result = msm.interactions.hbonds.get_hbonds(hbond_system(), pbc=False)
        item = next(
            item
            for item in result.parameters["attribution"]["items"]
            if item["id"] == paper
        )
        item["authors"][0] = "User edit"
        reported = next(
            item
            for item in json.loads(ackredit.report(format="json"))
            if item["id"] == paper
        )
        assert reported["authors"][0] == "Baker, E. N."
        fresh = msm.interactions.hbonds.get_hbonds(hbond_system(), pbc=False)
        fresh_item = next(
            item
            for item in fresh.parameters["attribution"]["items"]
            if item["id"] == paper
        )
        assert fresh_item["authors"][0] == "Baker, E. N."


def test_failed_detector_does_not_credit_successful_calculation():
    ackredit = pytest.importorskip("ackredit")
    molsys = hbond_system()
    with ackredit.session("failed-test"):
        with pytest.raises(msm.ArgumentError):
            msm.interactions.hbonds.get_hbonds(
                molsys, selection_mode="between", pbc=False
            )
        assert ackredit.get_used_items() == {}


def test_absent_ackredit_preserves_identical_result_metadata(monkeypatch):
    from molsysmt import _ackredit

    molsys = hbond_system()
    present = msm.interactions.hbonds.get_hbonds(molsys, pbc=False)
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    absent = msm.interactions.hbonds.get_hbonds(molsys, pbc=False)
    _assert_observations_equal(present, absent)


def test_broken_optional_provider_warns_and_preserves_completed_result(monkeypatch):
    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    molsys = hbond_system()
    expected = msm.interactions.hbonds.get_hbonds(molsys, pbc=False)

    def unavailable():
        raise ImportError("simulated broken provider")

    monkeypatch.setattr(_ackredit, "backend", unavailable)
    with pytest.warns(AckreditTrackingWarning, match="simulated broken provider"):
        actual = msm.interactions.hbonds.get_hbonds(molsys, pbc=False)
    _assert_observations_equal(actual, expected)


def test_result_bibliography_survives_all_persistence_paths_without_reader_tracking(
    tmp_path,
):
    ackredit = pytest.importorskip("ackredit")
    molsys = hbond_system()
    result = msm.interactions.hbonds.get_hbonds(molsys, pbc=False)
    original = deepcopy(result.parameters["attribution"])
    molsys.interactions = {"hydrogen_bonds": result}
    path = str(tmp_path / "with_analysis.h5msm")
    msm.convert(molsys, to_form=path)
    standalone = tmp_path / "analysis.h5msm"
    result.save(standalone)
    with ackredit.session("reader-test"):
        restored = msm.convert(path, to_form="molsysmt.MolSys").interactions[
            "hydrogen_bonds"
        ]
        typed = msm.convert(result, to_form="molsysmt.InteractionsDict")
        roundtrip = msm.convert(typed, to_form="molsysmt.Interactions")
        assert restored.parameters["attribution"] == original
        assert roundtrip.parameters["attribution"] == original
        assert msm.Interactions.load(standalone).parameters["attribution"] == original
        assert (
            result.remap(structure_indices=[2, 0]).parameters["attribution"] == original
        )
        assert (
            result.query(structure_indices=[2, 0]).parameters["attribution"] == original
        )
        assert ackredit.get_used_items() == {}


def test_real_viewer_preserves_original_bibliography_in_named_analyses_and_sessions(
    tmp_path,
):
    ackredit = pytest.importorskip("ackredit")
    msv = pytest.importorskip("molsysviewer")
    pytest.importorskip(
        "molsysviewer.interactions",
        reason="Experimental Viewer interactions API is required.",
    )
    molsys = hbond_system()
    with ackredit.session("viewer-producer"):
        result = msm.interactions.hbonds.get_hbonds(
            molsys, pbc=False, structure_indices=[2, 0, 1, 2]
        )
        original = deepcopy(result.parameters["attribution"])
        producer_versions = dict(result.software)
        paper = "doi:10.1016/0079-6107(84)90007-5"
        assert paper in ackredit.get_used_items()
        assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
        assert result.query(structure_indices=[1]).n_interactions == 0

    view = msv.new_view(molsys)
    try:
        with ackredit.session("viewer-reader"):
            view.interactions.attach(result, name="baker_hubbard", assume_aligned=True)
            metadata = view.interactions.analyses()[0]
            assert metadata["parameters"]["attribution"] == original
            assert metadata["software"] == producer_versions
            selected = view.interactions.query(
                "baker_hubbard", structure_indices=[2, 0, 2]
            )
            assert selected.parameters["attribution"] == original
            assert selected.n_interactions == 2

            complete = tmp_path / "viewer_complete.h5msm"
            analyses_only = tmp_path / "viewer_analyses.h5msm"
            session = tmp_path / "viewer_session.msv"
            msm.convert(view.molsys, to_form=str(complete))
            msm.h5msm.write_layers(
                str(analyses_only), interactions=dict(view.molsys.interactions)
            )
            view.save_session(session)

            for path in (complete, analyses_only):
                target = msv.new_view(hbond_system())
                try:
                    loaded = target.interactions.load(
                        path, analysis_name="baker_hubbard", assume_aligned=True
                    )
                    assert loaded.parameters["attribution"] == original
                    assert loaded.software == producer_versions
                    np.testing.assert_array_equal(
                        loaded.to_dict()["occurrence_indices"],
                        result.to_dict()["occurrence_indices"],
                    )
                    assert loaded.query(structure_indices=[1]).n_interactions == 0
                finally:
                    target.close()

            restored = msv.load_session(session)
            try:
                saved = restored.interactions.get_analysis("baker_hubbard")
                assert saved.parameters["attribution"] == original
                assert saved.software == producer_versions
                assert (
                    restored.interactions.analyses()[0]["parameters"]["attribution"]
                    == original
                )
            finally:
                restored.close()
            assert not any(
                "molsysmt.interactions" in caller
                for callers in ackredit.get_used_items().values()
                for caller in callers
            )
            assert paper not in ackredit.get_used_items()
    finally:
        view.close()


def test_lazy_import_and_genuine_provider_absence_in_fresh_process():
    script = """
import importlib.abc
import sys
class Absent(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "ackredit" or fullname.startswith("ackredit."):
            raise ModuleNotFoundError("Ackredit deliberately unavailable")
sys.meta_path.insert(0, Absent())
import molsysmt as msm
assert "ackredit" not in sys.modules
from rdkit import Chem
import numpy as np
molsys = msm.convert(Chem.AddHs(Chem.MolFromSmiles("O.O")), to_form="molsysmt.MolSys")
xyz = np.array([[[0, 0, 0], [.28, 0, 0], [.1, 0, 0], [0, .1, 0], [.28, .1, 0], [.28, 0, .1]]])
molsys.structures.append(coordinates=msm.pyunitwizard.quantity(xyz, "nm"))
result = msm.interactions.hbonds.get_hbonds(molsys, pbc=False)
assert result.n_interactions == 1
assert any(item.get("doi") == "10.1016/0079-6107(84)90007-5"
           for item in result.parameters["attribution"]["items"])
assert "ackredit" not in sys.modules
"""
    run = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
