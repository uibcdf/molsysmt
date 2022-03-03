from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
import numpy as np

def compare_n_structures_eq(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntaxis='MolSysMT'):

    report = {}

    from molsysmt.basic import get

    n_structures_A = get(molecular_system_A, target='system', selection=selection_A, structure_indices=structure_indices_A, n_structures=True, syntaxis=syntaxis)
    n_structures_B = get(molecular_system_B, target='system', selection=selection_B, structure_indices=structure_indices_B, n_structures=True, syntaxis=syntaxis)

    report['n_structures']=(n_structures_A==n_structures_B)

    # Report dictionary and result

    report = {key: value for key, value in report.items() if not value}
    result = (len(report)==0)

    return result, report

def compare_n_structures_in(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntaxis='MolSysMT'):

    raise NotImplementedError()

