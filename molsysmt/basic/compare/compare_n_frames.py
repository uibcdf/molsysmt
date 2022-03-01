from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
import numpy as np

def compare_n_frames_eq(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntaxis='MolSysMT'):

    report = {}

    from molsysmt.basic import get

    n_frames_A = get(molecular_system_A, target='system', selection=selection_A, structure_indices=structure_indices_A, n_frames=True, syntaxis=syntaxis)
    n_frames_B = get(molecular_system_B, target='system', selection=selection_B, structure_indices=structure_indices_B, n_frames=True, syntaxis=syntaxis)

    report['n_frames']=(n_frames_A==n_frames_B)

    # Report dictionary and result

    report = {key: value for key, value in report.items() if not value}
    result = (len(report)==0)

    return result, report

def compare_n_frames_in(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntaxis='MolSysMT'):

    raise NotImplementedError()

