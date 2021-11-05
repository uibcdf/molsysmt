from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
import numpy as np

def compare_n_elements_eq(molecular_system_A, molecular_system_B, selection_A='all',
        frame_indices_A='all', selection_B='all', frame_indices_B='all', syntaxis='MolSysMT'):

    report = {}

    from molsysmt.basic import get

    n_atoms_A, n_groups_A, n_components_A, n_chains_A, n_molecules_A, n_entities_A\
    = get(molecular_system_A, target='system', selection=selection_A, frame_indices=frame_indices_A,
            n_atoms=True, n_groups=True, n_components=True, n_chains=True, n_molecules=True,
            n_entities=True, syntaxis=syntaxis)

    n_atoms_B, n_groups_B, n_components_B, n_chains_B, n_molecules_B, n_entities_B\
    = get(molecular_system_B, target='system', selection=selection_B, frame_indices=frame_indices_B,
            n_atoms=True, n_groups=True, n_components=True, n_chains=True, n_molecules=True,
            n_entities=True, syntaxis=syntaxis)


    report['n_atoms']=(n_atoms_A==n_atoms_B)
    report['n_groups']=(n_groups_A==n_groups_B)
    report['n_components']=(n_components_A==n_components_B)
    report['n_chains']=(n_chains_A==n_chains_B)
    report['n_molecules']=(n_molecules_A==n_molecules_B)
    report['n_entities']=(n_entities_A==n_entities_B)

    # Report dictionary and result

    report = {key: value for key, value in report.items() if not value}
    result = (len(report)==0)

    return result, report

def compare_n_elements_in(molecular_system_A, molecular_system_B, selection_A='all',
        frame_indices_A='all', selection_B='all', frame_indices_B='all', syntaxis='MolSysMT'):

    raise NotImplementedError()

