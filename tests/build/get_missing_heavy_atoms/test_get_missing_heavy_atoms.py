"""
Unit and regression test for the is solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
import numpy as np
import sys

def test_get_missing_heavy_atoms_MolSys_1():

    molsys = msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'])
    missing_heavy_atoms = msm.build.get_missing_heavy_atoms(molsys)

    aux= {234: ['CG', 'CD', 'CE', 'NZ'],
          237: ['CG', 'OD1', 'OD2'],
          244: ['CD', 'OE1', 'OE2'],
          246: ['CG', 'CD', 'OE1', 'NE2'],
          254: ['CD', 'CE', 'NZ'],
          260: ['CG1', 'CG2'],
          264: ['CG', 'CD', 'CE', 'NZ'],
          282: ['OG'],
          325: ['O'],
          383: ['OE1', 'NE2'],
          385: ['NZ'],
          386: ['CG', 'CD', 'OE1', 'NE2'],
          422: ['NE', 'CZ', 'NH1', 'NH2'],
          429: ['CG', 'CD', 'OE1', 'NE2'],
          465: ['NE', 'CZ', 'NH1', 'NH2'],
          469: ['CG', 'CD', 'OE1', 'NE2'],
          471: ['CG', 'CD', 'CE', 'NZ'],
          472: ['CG', 'CD', 'OE1', 'NE2'],
          473: ['CG', 'CD1', 'CD2'],
          520: ['CD', 'CE', 'NZ'],
          526: ['CG', 'CD', 'OE1', 'OE2'],
          544: ['CG', 'CD', 'OE1', 'OE2'],
          562: ['CG', 'CD', 'OE1', 'OE2'],
          563: ['CG', 'OD1', 'ND2'],
          587: ['O']}

    assert missing_heavy_atoms == aux

