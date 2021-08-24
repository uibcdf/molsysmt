from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
from molsysmt.basic.get import get

def is_composed_of(molecular_system, selection='all', syntaxis='MolSysMT',
        n_ions=0, n_waters=0, n_cosolutes=0, n_small_molecules=0, n_peptides=0, n_proteins=0,
        n_dnas=0, n_rnas=0, n_lipids=0):

    n_ions_in, n_waters_in, n_cosolutes_in, n_small_molecules_in, n_peptides_in, n_proteins_in,\
    n_dnas_in, n_rnas_in, n_lipids_in = get(molecular_system, target="system", selection=selection,
            syntaxis=syntaxis, n_ions=True, n_waters=True, n_cosolutes=True,
            n_small_molecules=True, n_peptides=True, n_proteins=True, n_dnas=True, n_rnas=True,
            n_lipids=True)

    comparison = [[n_ions, n_ions_in], [n_waters, n_waters_in], [n_cosolutes, n_cosolutes_in],
            [n_small_molecules, n_small_molecules_in], [n_peptides, n_peptides_in], [n_proteins,
                n_proteins_in], [n_dnas, n_dnas_in], [n_rnas, n_rnas_in], [n_lipids, n_lipids_in]]

    output = True

    for condition, in_system in comparison:

        if type(condition)==int:
            if condition!=in_system:
                output = False
                break

        elif type(condition)==bool:
            if condition==True:
                if in_system==0:
                    output = False
                    break

    return output

