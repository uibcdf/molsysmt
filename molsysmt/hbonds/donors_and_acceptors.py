from molsysmt.multitool import select
from molsysmt._private_tools._digestion import digest_engine
from molsysmt._private_tools.exceptions import *
from molsysmt.covalent import covalent_chains
import numpy as np

acceptor_inclusion_rules = [
    "atom_type=='O'",
    "atom_type=='N'",
    "atom_type=='S'"
]

acceptor_exclusion_rules = [
    "atom_name=='NE2' and group_name=='GLN'",
    "(atom_name=='NE2' and group_name=='HIS') bonded to (atom_type=='H')",
    "(atom_name=='ND1' and group_name=='HIS') bonded to (atom_type=='H')",
]


donor_inclusion_rules = [
    "(atom_type=='O') bonded to (atom_type=='H')",
    "(atom_type=='N') bonded to (atom_type=='H')",
]

donor_exclusion_rules = [
    "(atom_name=='NE2') not bonded to (atom_type=='H')",
    "(atom_name=='ND1') not bonded to (atom_type=='H')",
]


def get_acceptor_atoms(molecular_system, selection='all',  inclusion_rules=[], exclusion_rules=[],
                       default_inclusion_rules=True, default_exclusion_rules=True, syntaxis='MolSysMT', engine='MolSysMT'):

    engine = digest_engine(engine)

    if engine=='MolSysMT':

        output = set()

        mask = select(molecular_system, selection=selection, syntaxis=syntaxis)

        if default_inclusion_rules:
            inclusion_rules += acceptor_inclusion_rules

        if default_exclusion_rules:
            exclusion_rules += acceptor_exclusion_rules

        for rule in inclusion_rules:
            tmp_acceptors = select(molecular_system, selection=rule, mask=mask, syntaxis=syntaxis)
            output.update(tmp_acceptors)

        for rule in exclusion_rules:
            tmp_not_acceptors = select(molecular_system, selection=rule, mask=mask, syntaxis=syntaxis)
            output.difference_update(tmp_not_acceptors)

        output = np.sort(list(output))

    else:

        raise NotImplementedError()

    return output

def get_donor_atoms(molecular_system, selection='all',  inclusion_rules=[], exclusion_rules=[],
                    default_inclusion_rules=True, default_exclusion_rules=True,
                    syntaxis='MolSysMT', engine='MolSysMT', with_Hs=False):

    engine = digest_engine(engine)

    if engine=='MolSysMT':

        output = set()

        mask = select(molecular_system, selection=selection, syntaxis=syntaxis)

        if default_inclusion_rules:
            inclusion_rules += donor_inclusion_rules

        if default_exclusion_rules:
            exclusion_rules += donor_exclusion_rules

        for rule in inclusion_rules:
            tmp_donors = select(molecular_system, selection=rule, mask=mask, syntaxis=syntaxis)
            output.update(tmp_donors)

        for rule in exclusion_rules:
            tmp_not_donors = select(molecular_system, selection=rule, mask=mask, syntaxis=syntaxis)
            output.difference_update(tmp_not_donors)

        output = covalent_chains(molecular_system, [output, 'atom_type=="H"'])
        output = np.sort(output, axis=0)

    else:

        raise NotImplementedError()

    return output

