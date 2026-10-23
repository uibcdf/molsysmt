"""Declared string prefixes select a candidate whose detector remains authoritative."""

from importlib import import_module

import pytest

import molsysmt as msm
from molsysmt.form import catalogue


@pytest.mark.parametrize(
    "item,expected",
    [
        ("pdb_id:1VII", "string:pdb_id"),
        ("amino_acids_1:ALYDERRRT", "string:amino_acids_1"),
        ("pdbqt_text:explicit but not yet parsed", "string:pdbqt_text"),
    ],
)
def test_declared_prefix_asks_only_its_own_detector(monkeypatch, item, expected):
    module = import_module("molsysmt.basic.get_form")
    original = module._asks
    asked = []

    def ask(form, value):
        asked.append(form)
        return original(form, value)

    monkeypatch.setattr(module, "_asks", ask)
    assert msm.get_form(item) == expected
    assert asked == [expected]


def test_rejected_prefix_candidate_still_uses_the_fallback(monkeypatch):
    module = import_module("molsysmt.basic.get_form")
    adapter = catalogue.module_of("string:pdbqt_text")
    monkeypatch.setattr(adapter, "is_form", lambda item: False)
    calls = []

    def fallback(item, *categories):
        calls.append((item, categories))
        return "string:pdb_text"

    monkeypatch.setattr(module, "_sweep", fallback)
    assert msm.get_form("pdbqt_text:rejected") == "string:pdb_text"
    assert calls == [("pdbqt_text:rejected", ("string", "file"))]


def test_prefix_detector_failure_keeps_its_original_cause(monkeypatch):
    adapter = catalogue.module_of("string:pdbqt_text")

    def broken(item):
        raise RuntimeError("the selected detector failed")

    monkeypatch.setattr(adapter, "is_form", broken)
    with pytest.raises(RuntimeError, match="the selected detector failed"):
        msm.get_form("pdbqt_text:declared")


def test_file_extension_retains_priority_over_a_string_prefix():
    assert msm.get_form("smiles:coordinates.pdb") == "file:pdb"


def test_prefix_matching_does_not_slice_or_partition_the_payload():
    class UnslicedString(str):
        def __getitem__(self, key):
            raise AssertionError("prefix lookup must not slice the payload")

        def partition(self, *args):
            raise AssertionError("prefix lookup must not partition the payload")

        def split(self, *args, **kwargs):
            raise AssertionError("prefix lookup must not split the payload")

    item = UnslicedString("pdbqt_text:" + "ATOM\n" * 100_000)
    assert catalogue._form_of_prefix(item) == "string:pdbqt_text"
    assert catalogue._form_of_prefix("unregistered_prefix:content") is None
