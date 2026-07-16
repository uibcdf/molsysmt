"""
Unit and regression test for the get_form module of the molsysmt package.
"""

import importlib

import molsysmt as msm
import pytest

from molsysmt._private.smonitor import UnknownAtomNameWarning


def test_atom_type_from_atom_name_1():
    assert 'H' == msm.element.atom.get_atom_type_from_atom_name('H1')
    assert 'C' == msm.element.atom.get_atom_type_from_atom_name('CB')
    assert 'O' == msm.element.atom.get_atom_type_from_atom_name('O2')
    assert 'N' == msm.element.atom.get_atom_type_from_atom_name('N')

def test_atom_type_from_atom_name_2(capsys):
    with pytest.warns(UnknownAtomNameWarning, match="XXX"):
        assert 'UNK' == msm.element.atom.get_atom_type_from_atom_name('XXX')

    assert capsys.readouterr().out == ""


def test_atom_type_from_atom_name_propagates_unexpected_mapping_errors(monkeypatch):
    module = importlib.import_module("molsysmt.element.atom.get_atom_type_from_atom_name")

    class BrokenMapping:
        def __getitem__(self, key):
            raise RuntimeError("mapping failure")

    monkeypatch.setattr(module, "atom_type_from_name", BrokenMapping())

    with pytest.raises(RuntimeError, match="mapping failure"):
        msm.element.atom.get_atom_type_from_atom_name("CA")
