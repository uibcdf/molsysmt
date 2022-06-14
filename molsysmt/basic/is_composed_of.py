from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molecular_system import is_molecular_system

def is_composed_of(molecular_system, selection='all', syntaxis='MolSysMT',
        ions=False, waters=False, cosolutes=False, small_molecules=False, peptides=False,
        proteins=False, dnas=False, rnas=False, lipids=False, check=True):

    from . import get

    if check:

        if not is_molecular_system(molecular_system):
            raise MolecularSystemNeededError()

        try:
            syntaxis = digest_syntaxis(syntaxis)
        except:
            raise WrongSyntaxisError(syntaxis)

        try:
            selection = digest_selection(selection, syntaxis)
        except:
            raise WrongSelectionError()

    n_ions_in, n_waters_in, n_cosolutes_in, n_small_molecules_in, n_peptides_in, n_proteins_in,\
    n_dnas_in, n_rnas_in, n_lipids_in = get(molecular_system, element="system", selection=selection,
            syntaxis=syntaxis, n_ions=True, n_waters=True, n_cosolutes=True,
            n_small_molecules=True, n_peptides=True, n_proteins=True, n_dnas=True, n_rnas=True,
            n_lipids=True, check=False)

    aux_list = [[ions, n_ions_in], [waters, n_waters_in], [cosolutes, n_cosolutes_in],
            [small_molecules, n_small_molecules_in], [peptides, n_peptides_in], [proteins,
                n_proteins_in], [dnas, n_dnas_in], [rnas, n_rnas_in], [lipids, n_lipids_in]]

    output = True

    for condition, in_system in aux_list:

        if type(condition)==int:
            if condition!=in_system:
                output = False
                break

        elif type(condition)==bool:
            if condition==True:
                if in_system==0:
                    output = False
                    break
            else:
                if in_system>0:
                    output = False
                    break

    return output

