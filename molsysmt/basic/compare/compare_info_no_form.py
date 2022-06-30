from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def compare_info_no_form_eq(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntaxis='MolSysMT'):

    report = {}

    from .. import get, get_form

    form_A = get_form(molecular_system_A)
    form_B = get_form(molecular_system_B)

    n_atoms_A, n_groups_A, n_components_A, n_chains_A, n_molecules_A, n_entities_A, n_structures_A,\
    n_ions_A, n_waters_A, n_cosolutes_A, n_small_molecules_A, n_peptides_A, n_proteins_A, n_dnas_A,\
    n_rnas_A, n_lipids_A = get(molecular_system_A, element='system', selection=selection_A,
                               structure_indices=structure_indices_A, syntaxis=syntaxis, n_atoms=True, n_groups=True,
                               n_components=True, n_chains=True, n_molecules=True, n_entities=True, n_structures=True,
                               n_ions=True, n_waters=True, n_cosolutes=True, n_small_molecules=True, n_peptides=True,
                               n_proteins=True, n_dnas=True, n_rnas=True, n_lipids=True)

    n_atoms_B, n_groups_B, n_components_B, n_chains_B, n_molecules_B, n_entities_B, n_structures_B,\
    n_ions_B, n_waters_B, n_cosolutes_B, n_small_molecules_B, n_peptides_B, n_proteins_B, n_dnas_B,\
    n_rnas_B, n_lipids_B = get(molecular_system_B, element='system', selection=selection_B,
                               structure_indices=structure_indices_B, syntaxis=syntaxis, n_atoms=True, n_groups=True,
                               n_components=True, n_chains=True, n_molecules=True, n_entities=True, n_structures=True,
                               n_ions=True, n_waters=True, n_cosolutes=True, n_small_molecules=True, n_peptides=True,
                               n_proteins=True, n_dnas=True, n_rnas=True, n_lipids=True)

    report['n_atoms']=(n_atoms_A==n_atoms_B)
    report['n_groups']=(n_groups_A==n_groups_B)
    report['n_components']=(n_components_A==n_components_B)
    report['n_chains']=(n_chains_A==n_chains_B)
    report['n_molecules']=(n_molecules_A==n_molecules_B)
    report['n_entities']=(n_entities_A==n_entities_B)
    report['n_structures']=(n_structures_A==n_structures_B)
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

def compare_info_no_form_in(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntaxis='MolSysMT'):

    raise NotImplementedError()

