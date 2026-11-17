"""Receive the saved result projection with Ackredit's actual public reader."""

import json
import subprocess
import sys
from copy import deepcopy

import pytest

import molsysmt as msm
from tests.interactions.hbonds.test_attributed_hbonds import _system
from tests.interactions.test_scientific_attribution import _assert_observations_equal


def test_two_results_keep_portable_references_roles_and_original_versions():
    ackredit = pytest.importorskip("ackredit", minversion="0.9.0")

    paper = "doi:10.1016/0079-6107(84)90007-5"
    with ackredit.session("portable-interaction-workflow"):
        with ackredit.capture("first-analysis") as first_capture:
            first = msm.interactions.hbonds.get_hbonds(
                _system(), pbc=False, structure_indices=[2, 0, 2]
            )
        with ackredit.capture("empty-analysis") as empty_capture:
            empty = msm.interactions.hbonds.get_hbonds(
                _system(), pbc=False, structure_indices=[1]
            )
        for result, capture in [(first, first_capture), (empty, empty_capture)]:
            wrapper = result.parameters["attribution"]
            assert wrapper["schema"] == "molsysmt.scientific_attribution@1"
            portable = ackredit.Attribution.from_dict(wrapper["portable"]).to_dict()
            records = {item["id"]: item for item in portable["items"]}
            assert records[paper]["authors"] == ["Baker, E. N.", "Hubbard, R. E."]
            original_version = result.software["molsysmt"]
            assert (
                records[f"software:molsysmt:{original_version}"]["version"]
                == original_version
            )
            assert portable["context"]["software"] == result.software
            assert portable["context"]["method"] == "baker_hubbard"
            assert portable["context"]["attribution_scope"] == "result_bibliography"
            declared = next(use for use in portable["uses"] if use["item_id"] == paper)
            observed = next(
                use
                for use in capture.attribution.to_dict()["uses"]
                if use["item_id"] == paper and use["used_by"] == wrapper["target"]
            )
            assert declared["roles"] == observed["roles"] == ["scientific_criterion"]
            assert declared["context"] == observed["context"]
            assert portable["usage_tree"][wrapper["target"]]["children"] == []
        assert paper in ackredit.get_used_items()
        assert paper in {
            item["id"] for item in ackredit.get_attribution().to_dict()["items"]
        }
    assert empty.n_interactions == 0
    assert empty.evaluated_structure_indices.tolist() == [1]


def test_provider_absence_keeps_identical_portable_metadata_and_science(monkeypatch):
    from molsysmt import _ackredit

    ackredit = pytest.importorskip("ackredit", minversion="0.9.0")
    with ackredit.session("portable-present"):
        expected = msm.interactions.hbonds.get_hbonds(_system(), pbc=False)
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    absent = msm.interactions.hbonds.get_hbonds(_system(), pbc=False)
    _assert_observations_equal(expected, absent)
    assert (
        ackredit.Attribution.from_dict(
            absent.parameters["attribution"]["portable"]
        ).to_dict()
        == expected.parameters["attribution"]["portable"]
    )


def test_portable_result_records_are_detached_from_legacy_and_other_results():
    first = msm.interactions.hbonds.get_hbonds(_system(), pbc=False)
    second = msm.interactions.hbonds.get_hbonds(_system(), pbc=False)
    original = deepcopy(second.parameters["attribution"])
    attribution = first.parameters["attribution"]
    attribution["portable"]["items"][0]["title"] = "changed locally"
    attribution["portable"]["uses"][0]["context"]["software"]["molsysmt"] = "local"
    attribution["portable"]["context"]["software"]["molsysmt"] = "other local"
    assert attribution["items"] == original["items"]
    assert second.parameters["attribution"] == original
    assert first.software == second.software


@pytest.mark.parametrize("format_version", [None, "0.5"])
def test_portable_payload_survives_typed_named_and_analysis_only_storage(
    tmp_path, format_version
):
    ackredit = pytest.importorskip("ackredit", minversion="0.9.0")

    molsys = _system()
    result = msm.interactions.hbonds.get_hbonds(molsys, pbc=False)
    original = deepcopy(result.parameters["attribution"])
    molsys.interactions = {"original": result}
    path = tmp_path / "named.h5msm"
    options = {} if format_version is None else {"format_version": format_version}
    msm.h5msm.write(molsys, path, **options)
    standalone = tmp_path / "analysis.h5msm"
    result.save(standalone)
    typed = msm.convert(result, to_form="molsysmt.InteractionsDict")
    with ackredit.session("portable-detached-reader"):
        restored = [
            msm.h5msm.read(path).interactions["original"],
            msm.Interactions.load(standalone),
            msm.convert(typed, to_form="molsysmt.Interactions"),
            result.query(structure_indices=[2, 0]),
            result.remap(structure_indices=[2, 0]),
        ]
        for analysis in restored:
            assert analysis.parameters["attribution"] == original
            detached = ackredit.Attribution.from_dict(original["portable"])
            assert "Baker" in detached.report(format="bibtex")
            assert detached.to_dict() == original["portable"]
        assert ackredit.get_used_items() == {}


def test_fresh_reader_needs_no_scientific_producer_and_adds_no_credit(tmp_path):
    pytest.importorskip("ackredit", minversion="0.9.0")
    result = msm.interactions.hbonds.get_hbonds(_system(), pbc=False)
    payload = result.parameters["attribution"]["portable"]
    source = tmp_path / "attribution.json"
    source.write_text(json.dumps(payload))
    script = """
import importlib.abc, json, sys
from pathlib import Path
class NoProducer(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'molsysmt','rdkit','mdtraj','openmm'}:
            raise AssertionError('Scientific producer imported while reading: '+fullname)
sys.meta_path.insert(0,NoProducer())
import ackredit
saved=json.loads(Path(sys.argv[1]).read_text())
with ackredit.session('fresh-reader'):
    detached=ackredit.Attribution.from_dict(saved)
    assert detached.to_dict()==saved
    assert 'Baker' in detached.report(format='bibtex')
    assert ackredit.get_used_items()=={}
assert not any(name.split('.')[0] in {'molsysmt','rdkit','mdtraj','openmm'} for name in sys.modules)
"""
    subprocess.run([sys.executable, "-c", script, str(source)], check=True)
