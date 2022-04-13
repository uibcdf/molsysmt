from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def contains(molecular_system, selection='all', syntaxis='MolSysMT',
        ions=None, waters=None, cosolutes=None, small_molecules=None, peptides=None, proteins=None,
        dnas=None, rnas=None, lipids=None, check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection, syntaxis)

    from . import get

    n_ions_in, n_waters_in, n_cosolutes_in, n_small_molecules_in, n_peptides_in, n_proteins_in,\
    n_dnas_in, n_rnas_in, n_lipids_in = get(molecular_system, target="system", selection=selection,
            syntaxis=syntaxis, n_ions=True, n_waters=True, n_cosolutes=True,
            n_small_molecules=True, n_peptides=True, n_proteins=True, n_dnas=True, n_rnas=True,
            n_lipids=True, check=False)

    aux_list = [[ions, n_ions_in], [waters, n_waters_in], [cosolutes, n_cosolutes_in],
            [small_molecules, n_small_molecules_in], [peptides, n_peptides_in], [proteins,
                n_proteins_in], [dnas, n_dnas_in], [rnas, n_rnas_in], [lipids, n_lipids_in]]

    output = True

    for condition, in_system in aux_list:

        if condition is not None:
            if type(condition)==bool:
                if condition==True and in_system==0:
                    output = False
                    break
                elif condition==False and in_system>0:
                    output = False
                    break
            elif type(condition)==int:
                if condition>in_system:
                    output = False
                    break

    return output

