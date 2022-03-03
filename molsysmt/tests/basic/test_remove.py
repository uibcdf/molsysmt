"""
Unit and regression test for the remove module of the molsysmt package.
"""

import molsysmt as msm
import numpy as np
from pandas import DataFrame

def test_remove_1():

    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.remove(molsys, selection='chain_index==[1,2,3]')
    df = msm.info(molsys)
    true_dict = {'form': {0: 'molsysmt.MolSys'},
                 'n_atoms': {0: 1906},
                 'n_groups': {0: 248},
                 'n_components': {0: 1},
                 'n_chains': {0: 1},
                 'n_molecules': {0: 1},
                 'n_entities': {0: 1},
                 'n_proteins': {0: 1},
                 'n_structures': {0: 1}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_remove_2():

    molsys = msm.demo['Trp-Cage']['1l2y.pdb']
    molsys = msm.convert(molsys, to_form='molsysmt.Trajectory')
    molsys = msm.remove(molsys, structure_indices=range(1,38))
    df = msm.info(molsys)
    true_dict = {'form': {0: 'molsysmt.Trajectory'},
                 'n_atoms': {0: 304},
                 'n_groups': {0: None},
                 'n_components': {0: None},
                 'n_chains': {0: None},
                 'n_molecules': {0: None},
                 'n_entities': {0: None},
                 'n_structures': {0: 1}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)


