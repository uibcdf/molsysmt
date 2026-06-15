"""Unit and regression test for ``molsysmt.physchem.get_electronegativity``."""

import os
import tempfile

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def test_get_electronegativity_pauling_on_protein():
    molsys = msm.convert(
        msm.systems['T4 lysozyme L99A']['181l.pdb'],
        selection='molecule_type=="protein"',
    )
    en = puw.get_value(msm.physchem.get_electronegativity(molsys, element='atom'))
    elements = msm.get(molsys, element='atom', atom_type=True)
    by_element = {}
    for symbol, value in zip(elements, en):
        by_element.setdefault(symbol, float(value))
    # Standard Pauling electronegativities.
    assert by_element['C'] == pytest.approx(2.55)
    assert by_element['N'] == pytest.approx(3.04)
    assert by_element['O'] == pytest.approx(3.44)
    assert by_element['S'] == pytest.approx(2.58)


def test_get_electronegativity_nan_for_dummy_element():
    pdb = (
        "HETATM    1 X    X   A   1       0.000   0.000   0.000  1.00  0.00           X\n"
        "END\n"
    )
    fd, path = tempfile.mkstemp(suffix='.pdb')
    try:
        os.write(fd, pdb.encode())
    finally:
        os.close(fd)
    try:
        molsys = msm.convert(path, to_form='molsysmt.MolSys')
    finally:
        os.remove(path)
    en = puw.get_value(msm.physchem.get_electronegativity(molsys, element='atom'))
    assert np.isnan(en[0])


def test_get_electronegativity_rejects_unknown_definition():
    molsys = msm.convert(
        msm.systems['T4 lysozyme L99A']['181l.pdb'],
        selection='molecule_type=="protein"',
    )
    with pytest.raises(Exception):
        msm.physchem.get_electronegativity(molsys, element='atom', definition='nope')
