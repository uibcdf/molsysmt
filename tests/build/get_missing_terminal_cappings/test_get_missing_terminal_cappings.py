"""
Unit and regression test for the is solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
import numpy as np
import sys

def test_get_missing_terminal_cappings_MolSys_1():

    molsys = msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'])
    missing_cappings = msm.build.get_missing_terminal_cappings(molsys)

    assert len(missing_cappings) == 1
    assert missing_cappings[412] == ['OXT']

