"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np


def test_get_buch_hbonds_1(barnase_barstar_molsys):

    molsys = barnase_barstar_molsys

    hbonds, distance = msm.hbonds.get_buch_hbonds(molsys, selection='molecule_name=="BARNASE"',
                                                  selection_2='molecule_name=="BARSTAR"')

    good_hbonds = [[ 431,  432, 2400],
                   [ 431,  433, 2361],
                   [ 858,  859, 2296],
                   [ 876,  878, 2969],
                   [ 879,  880, 2969],
                   [ 882,  883, 2297],
                   [1253, 1254, 2412],
                   [1253, 1255, 2361],
                   [1256, 1258, 2361],
                   [1256, 1258, 2362],
                   [1311, 1312, 2362],
                   [1317, 1319, 2362],
                   [1568, 1569, 2194],
                   [1610, 1612, 2237],
                   [2264, 2266, 1563],
                   [2267, 2268,  896]]

    all_good = True

    for ii,jj in zip(hbonds[0], good_hbonds):
        if not np.all(ii==jj):
            all_good = False
            break

    assert all_good


def test_get_buch_hbonds_2(hp35_molsys):

    molsys = hp35_molsys
    hbonds, distance = msm.hbonds.get_buch_hbonds(molsys)

    good_hbonds = [[ 42,  43,  91],
                   [ 51,  52,  90],
                   [ 80,  81,  90],
                   [ 92,  93,  47],
                   [112, 113,  58],
                   [130, 131,  78],
                   [130, 133,  79],
                   [134, 135,  70],
                   [144, 145,  85],
                   [160, 161,  97],
                   [180, 181, 117],
                   [187, 188, 165],
                   [218, 219,  64],
                   [236, 237,  28],
                   [236, 238,  63],
                   [239, 241,  28],
                   [253, 254, 212],
                   [263, 264, 209],
                   [293, 294, 258],
                   [307, 308, 268],
                   [383, 384, 330],
                   [401, 402, 530],
                   [401, 403, 529],
                   [405, 406, 330],
                   [419, 420, 268],
                   [422, 423, 345],
                   [439, 440, 364],
                   [453, 454, 388],
                   [472, 473, 410],
                   [490, 491,   1],
                   [490, 492, 559],
                   [494, 495, 458],
                   [512, 513, 477],
                   [512, 514, 435],
                   [512, 515, 427],
                   [516, 517, 444],
                   [531, 532, 458],
                   [549, 550, 149]]

    all_good = True

    for ii,jj in zip(hbonds[0], good_hbonds):
        if not np.all(ii==jj):
            all_good = False
            break

    assert all_good
