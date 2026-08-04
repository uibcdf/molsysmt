from molsysmt._private.arg_digestion import arg_digest
import numpy as np


donor_inclusion_rules = [
    "(atom_type=='O') bonded to (atom_type=='H')",
    "(atom_type=='N') bonded to (atom_type=='H')",
]

donor_exclusion_rules = [
    "(atom_name=='NE2') not bonded to (atom_type=='H')",
    "(atom_name=='ND1') not bonded to (atom_type=='H')",
]

@arg_digest()
def get_donor_atoms(molecular_system, selection='all',  inclusion_rules=None, exclusion_rules=None,
                    default_inclusion_rules=True, default_exclusion_rules=True,
                    syntax='MolSysMT'):
    """
    Identify donor atoms (and their hydrogens) for hydrogen-bond detection.

    Parameters
    ----------
    molecular_system : molecular system
        Input system.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atom selection to filter candidates.
    inclusion_rules, exclusion_rules : list of str or None
        Selection rules to include or exclude atoms.
    default_inclusion_rules, default_exclusion_rules : bool, default True
        Whether to apply built-in donor rules.
    syntax : str, default 'MolSysMT'
        Selection syntax for string rules.

    Returns
    -------
    numpy.ndarray
        Array of donor–hydrogen pairs (shape `(n, 2)`).
    """

    from molsysmt import select
    from molsysmt.topology import get_covalent_paths

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

    output = get_covalent_paths(molecular_system, [list(output), 'atom_type=="H"'])
    output = np.sort(output, axis=0)

    return output
