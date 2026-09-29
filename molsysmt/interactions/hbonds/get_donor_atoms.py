import numpy as np

from molsysmt._private.argdigest import arg_digest

donor_inclusion_rules = [
    "(atom_type=='O') bonded to (atom_type=='H')",
    "(atom_type=='N') bonded to (atom_type=='H')",
]

donor_exclusion_rules = [
    "(atom_name=='NE2') not bonded to (atom_type=='H')",
    "(atom_name=='ND1') not bonded to (atom_type=='H')",
]


@arg_digest()
def get_donor_atoms(
    molecular_system,
    selection="all",
    inclusion_rules=None,
    exclusion_rules=None,
    default_inclusion_rules=True,
    default_exclusion_rules=True,
    syntax="MolSysMT",
):
    """
    Identifying donor atoms and their covalently attached hydrogens.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    inclusion_rules : list of str or None, default=None
        Additional atom-selection rules identifying donor heavy atoms.
    exclusion_rules : list of str or None, default=None
        Additional atom-selection rules excluding donor heavy atoms.
    default_inclusion_rules : bool, default=True
        Whether to apply default chemical inclusion rules.
    default_exclusion_rules : bool, default=True
        Whether to apply default chemical exclusion rules.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').

    Returns
    -------
    numpy.ndarray
        Integer array of covalently bonded donor–hydrogen pairs with shape
        ``(n, 2)``, sorted by donor and then hydrogen index. Row sorting keeps
        each covalent pair intact even when the two index orders differ.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.interactions.hbonds.get_donor_atoms import get_donor_atoms
    >>> builder = msm.MolSysBuilder()
    >>> _ = [builder.add_atom(atom_name=name, atom_type=kind) for name, kind in
    ...      [("N1", "N"), ("H2", "H"), ("N2", "N"), ("H1", "H")]]
    >>> _ = builder.add_group([0, 1, 2, 3], group_name="ALA")
    >>> _ = builder.add_bond(0, 3)
    >>> _ = builder.add_bond(2, 1)
    >>> get_donor_atoms(builder.build()).tolist()
    [[0, 3], [2, 1]]

    .. admonition:: User guide

       See :ref:`Tutorial_Get_donor_atoms` for selecting covalent donor pairs.

    .. versionadded:: 1.0.0
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
        tmp_not_donors = select(
            molecular_system, selection=rule, mask=mask, syntax=syntax
        )
        output.difference_update(tmp_not_donors)

    if not output:
        return np.empty((0, 2), dtype=np.int64)

    output = get_covalent_paths(molecular_system, [list(output), 'atom_type=="H"'])
    output = output[np.lexsort((output[:, 1], output[:, 0]))]

    return output
