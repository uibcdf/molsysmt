from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def compare_form_eq(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntax='MolSysMT'):

    report = {}

    from .. import get, get_form

    form_A = get_form(molecular_system_A)
    form_B = get_form(molecular_system_B)

    report['forms']=(form_A==form_B)

    # Report dictionary and result

    report = {key: value for key, value in report.items() if not value}
    result = (len(report)==0)

    return result, report

def compare_form_in(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntax='MolSysMT'):

    raise NotImplementedError()

