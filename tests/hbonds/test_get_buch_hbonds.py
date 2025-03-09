"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np


def test_get_buch_hbonds_1():

    molsys = msm.convert(msm.systems['Barnase-Barstar']['barnase_barstar.h5msm'])

    hbonds, distance = msm.hbonds.get_buch_hbonds(molsys, selection='molecule_name=="BARNASE"',
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
                   [1256, 1258, 2362],
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


def test_get_buch_hbonds_2():

    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'])
    hbonds, distance = msm.hbonds.get_buch_hbonds(molsys)

    good_hbonds = [[ 42,  43,  91],
                   [ 51,  52,  90],
                   [ 80,  81,  90],
                   [ 92,  93,  47],
                   [112, 113,  58],
                   [130, 131,  78],
                   [130, 132,  79],
                   [134, 135,  70],
                   [144, 145,  85],
                   [160, 161,  97],
                   [180, 181, 117],
                   [187, 188, 165],
                   [218, 219,  64],
                   [233, 234,  63],
                   [236, 237,  28],
                   [239, 240,  28],
                   [239, 241,  63],
                   [253, 254, 212],
                   [263, 264, 209],
                   [283, 284, 223],
                   [293, 294, 258],
                   [307, 308, 268],
                   [383, 384, 330],
                   [401, 402, 529],
                   [401, 404, 530],
                   [405, 406, 330],
                   [419, 420, 268],
                   [422, 423, 345],
                   [439, 440, 364],
                   [453, 454, 388],
                   [472, 473, 410],
                   [490, 491,   1],
                   [490, 493, 559],
                   [494, 495, 458],
                   [512, 513, 427],
                   [512, 514, 477],
                   [512, 515, 435],
                   [516, 517, 444],
                   [531, 532, 458],
                   [549, 550, 149],
                   [579, 580, 560]]

    all_good = True

    for ii,jj in zip(hbonds[0], good_hbonds):
        if not np.all(ii==jj):
            all_good = False
            break

    assert all_good

