from molsysmt._private.digestion import digest
import numpy as np


donor_inclusion_rules = [
    "(atom_type=='O') bonded to (atom_type=='H')",
    "(atom_type=='N') bonded to (atom_type=='H')",
]

donor_exclusion_rules = [
    "(atom_name=='NE2') not bonded to (atom_type=='H')",
    "(atom_name=='ND1') not bonded to (atom_type=='H')",
]

@digest()
def get_donor_atoms(molecular_system, selection='all',  inclusion_rules=None, exclusion_rules=None,
                    default_inclusion_rules=True, default_exclusion_rules=True,
                    syntax='MolSysMT'):

    from molsysmt import select
    from molsysmt.topology import get_covalent_chains

    output = set()

    mask = select(molecular_system, selection=selection, syntax=syntax)

    if default_inclusion_rules:
        inclusion_rules += donor_inclusion_rules

    if default_exclusion_rules:
        exclusion_rules += donor_exclusion_rules

    for rule in inclusion_rules:
        tmp_donors = select(molecular_system, selection=rule, mask=mask, syntax=syntax)
        output.update(tmp_donors)

    for rule in exclusion_rules:
        tmp_not_donors = select(molecular_system, selection=rule, mask=mask, syntax=syntax)
        output.difference_update(tmp_not_donors)

    output = get_covalent_chains(molecular_system, [list(output), 'atom_type=="H"'])
    output = np.sort(output, axis=0)

    return output

