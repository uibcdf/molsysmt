"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np


def test_get_luzard_chandler_hbonds():

    molsys = msm.convert(msm.systems['Barnase-Barstar']['barnase_barstar.h5msm'])

    hbonds, distance, angles = msm.hbonds.get_luzard_chandler_hbonds(molsys, selection='molecule_name=="BARNASE"',
                                              selection_2='molecule_name=="BARSTAR"')

    good_hbonds = [[ 431,  432, 2361],
                   [ 431,  433, 2400],
                   [ 583,  584, 2442],
                   [ 858,  859, 2296],
                   [ 876,  877, 2969],
                   [ 879,  880, 2969],
                   [ 882,  883, 2297],
                   [1253, 1254, 2412],
                   [1253, 1255, 2361],
                   [1256, 1258, 2361],
                   [1311, 1312, 2362],
                   [1317, 1319, 2362],
                   [1568, 1569, 2194],
                   [1610, 1612, 2237],
                   [2264, 2265, 1563],
                   [2267, 2268,  896]]

    all_good = True

    for ii,jj in zip(hbonds[0], good_hbonds):
        if not np.all(ii==jj):
            all_good = False
            break

    assert all_good

