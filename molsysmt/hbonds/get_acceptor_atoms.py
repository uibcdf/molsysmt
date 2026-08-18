from molsysmt._private.argdigest import arg_digest
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

@arg_digest()
def get_acceptor_atoms(molecular_system, selection='all', inclusion_rules=None,
        exclusion_rules=None, default_inclusion_rules=True, default_exclusion_rules=True,
        syntax='MolSysMT'):
    """
    Identify acceptor atoms within a molecular system for hydrogen-bond detection.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    inclusion_rules : dict, default=None
        Custom inclusion rules dictionary for hydrogen bond detection.
    exclusion_rules : dict, default=None
        Custom exclusion rules dictionary for hydrogen bond detection.
    default_inclusion_rules : bool, default=True
        Whether to apply default chemical inclusion rules.
    default_exclusion_rules : bool, default=True
        Whether to apply default chemical exclusion rules.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').

    Returns
    -------
    numpy.ndarray
        Sorted array of acceptor atom indices.
    """

    from molsysmt import select

    output = set()

    mask = select(molecular_system, selection=selection, syntax=syntax)

    if default_inclusion_rules:
        inclusion_rules += acceptor_inclusion_rules

    if default_exclusion_rules:
        exclusion_rules += acceptor_exclusion_rules

    for rule in inclusion_rules:
        tmp_acceptors = select(molecular_system, selection=rule, mask=mask, syntax=syntax)
        output.update(tmp_acceptors)

    for rule in exclusion_rules:
        tmp_not_acceptors = select(molecular_system, selection=rule, mask=mask, syntax=syntax)
        output.difference_update(tmp_not_acceptors)

    output = np.sort(list(output))

    return output
