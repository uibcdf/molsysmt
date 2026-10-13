"""Verify detached inspiration records and real optional Ackredit observation."""

import json
import pickle
import subprocess
import sys

import numpy as np
import pytest

import molsysmt as msm
from tests.structure.test_get_symmetry_corrected_rmsd import system

PAPER = "doi:10.1186/s13321-019-0362-7"


def test_real_capture_records_roles_reused_results_and_enclosing_workflow():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("symmetry-workflow"):
        with ackredit.scope("dockingmt.evaluate"):
            with ackredit.capture("first") as first:
                graph = msm.topology.get_atom_correspondences("smiles:c1ccccc1")
            with ackredit.capture("second") as second:
                result = msm.structure.get_symmetry_corrected_rmsd(
                    system(), structure_indices=[]
                )
        for capture in (first, second):
            saved = capture.attribution.to_dict()
            paper = next(item for item in saved["items"] if item["id"] == PAPER)
            assert paper["authors"] == ["Bell, Eric W.", "Zhang, Yang"]
            uses = [use for use in saved["uses"] if use["item_id"] == PAPER]
            assert uses and all(
                use["roles"] == ["methodological_inspiration"] for use in uses
            )
            assert not any(
                "reference_implementation" in use["roles"] for use in saved["uses"]
            )
            software = [
                item
                for item in saved["items"]
                if item["id"].startswith("software:rdkit:")
            ]
            assert len(software) == 1
        assert graph["attribution"]["items"] and result["attribution"]["items"]
        assert PAPER in ackredit.get_used_items()
        assert (
            "molsysmt.topology.get_atom_correspondences"
            in ackredit.current_session().usage_tree["dockingmt.evaluate"]["children"]
        )


def test_faithful_stereo_backend_is_credited_only_when_labels_are_used():
    plain = msm.topology.get_atom_correspondences("smiles:c1ccccc1")
    chiral = msm.topology.get_atom_correspondences("smiles:C[C@H](O)F")
    paper = "doi:10.1021/acs.jcim.8b00324"
    assert paper not in {item["id"] for item in plain["attribution"]["items"]}
    reference = next(item for item in chiral["attribution"]["items"] if item["id"] == paper)
    assert reference["roles"] == ["scientific_criterion"]
    assert len(reference["authors"]) == 6


def test_absent_provider_preserves_science_and_detached_bibliography(monkeypatch):
    from molsysmt import _ackredit

    molsys = system()
    observed = msm.structure.get_symmetry_corrected_rmsd(molsys)
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    absent = msm.structure.get_symmetry_corrected_rmsd(molsys)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(absent["rmsd"]),
        msm.pyunitwizard.get_value(observed["rmsd"]),
    )
    assert absent["attribution"] == observed["attribution"]
    assert json.loads(json.dumps(absent["attribution"])) == absent["attribution"]


def test_provider_failure_preserves_completed_science_and_emits_diagnostic(monkeypatch):
    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    def fail():
        raise RuntimeError("attribution provider unavailable")

    monkeypatch.setattr(_ackredit, "backend", fail)
    with pytest.warns(AckreditTrackingWarning):
        result = msm.topology.get_atom_correspondences("smiles:c1ccccc1")
    assert result["atom_correspondences"].shape == (12, 6, 2)


def test_reading_result_retains_original_versions_without_new_credit():
    ackredit = pytest.importorskip("ackredit")
    result = msm.structure.get_symmetry_corrected_rmsd(system())
    encoded = pickle.dumps(result)
    with ackredit.session("reader"):
        restored = pickle.loads(encoded)
        assert restored["attribution"] == result["attribution"]
        assert restored["software"] == result["software"]
        assert not ackredit.get_used_items()


def test_failed_science_earns_no_completed_correspondence_credit():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("failed-correspondence"):
        with pytest.raises(msm.StructuralInconsistencyError):
            msm.topology.get_atom_correspondences("smiles:CC(O)F")
        assert not ackredit.get_used_items()


def test_fresh_import_is_lazy_and_genuine_ackredit_absence_keeps_result():
    script = """
import sys
from importlib.abc import MetaPathFinder
from unittest.mock import patch
import molsysmt as msm
from depdigest import is_installed
from depdigest.core import checker
assert 'ackredit' not in sys.modules
original = checker.find_spec
def absent(name, *args, **kwargs):
    return None if name == 'ackredit' else original(name, *args, **kwargs)
class RefuseAckredit(MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'ackredit' or fullname.startswith('ackredit.'):
            raise ImportError('Ackredit absent in this controlled interpreter')
sys.meta_path.insert(0, RefuseAckredit())
with patch.object(checker, 'find_spec', absent):
    is_installed.cache_clear()
    result = msm.topology.get_atom_correspondences('smiles:c1ccccc1')
    assert result['atom_correspondences'].shape == (12, 6, 2)
    assert result['attribution']['items']
assert 'ackredit' not in sys.modules
"""
    completed = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=60
    )
    assert completed.returncode == 0, completed.stderr
