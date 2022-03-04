from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
import numpy as np

def compare_n_molecules_eq(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntaxis='MolSysMT'):

    report = {}

    from molsysmt.basic import get

    n_ions_A, n_waters_A, n_cosolutes_A, n_small_molecules_A, n_peptides_A, n_proteins_A, n_dnas_A,\
    n_rnas_A, n_lipids_A = get(molecular_system_A, target='system', selection=selection_A, structure_indices=structure_indices_A,
            n_ions=True, n_waters=True, n_cosolutes=True, n_small_molecules=True,
            n_peptides=True, n_proteins=True, n_dnas=True, n_rnas=True, n_lipids=True)

    n_ions_B, n_waters_B, n_cosolutes_B, n_small_molecules_B, n_peptides_B, n_proteins_B, n_dnas_B,\
    n_rnas_B, n_lipids_B = get(molecular_system_A, target='system', selection=selection_B, structure_indices=structure_indices_B,
            n_ions=True, n_waters=True, n_cosolutes=True, n_small_molecules=True,
            n_peptides=True, n_proteins=True, n_dnas=True, n_rnas=True, n_lipids=True)

    report['n_ions']=(n_ions_A==n_ions_B)
    report['n_waters']=(n_waters_A==n_waters_B)
    report['n_cosolutes']=(n_cosolutes_A==n_cosolutes_B)
    report['n_small_molecules']=(n_small_molecules_A==n_small_molecules_B)
    report['n_peptides']=(n_peptides_A==n_peptides_B)
    report['n_proteins']=(n_proteins_A==n_proteins_B)
    report['n_dnas']=(n_dnas_A==n_dnas_B)
    report['n_rnas']=(n_rnas_A==n_rnas_B)
    report['n_lipids']=(n_lipids_A==n_lipids_B)

    # Report dictionary and result

    report = {key: value for key, value in report.items() if not value}
    result = (len(report)==0)

    return result, report

def compare_n_molecules_in(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntaxis='MolSysMT'):

    raise NotImplementedError()

