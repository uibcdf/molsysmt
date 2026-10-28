import numpy as np

from molsysmt._private.argdigest import arg_digest

acceptor_inclusion_rules = ["atom_type=='O'", "atom_type=='N'", "atom_type=='S'"]

acceptor_exclusion_rules = [
    "atom_name=='NE2' and group_name=='GLN'",
    "(atom_name=='NE2' and group_name=='HIS') bonded to (atom_type=='H')",
    "(atom_name=='ND1' and group_name=='HIS') bonded to (atom_type=='H')",
]


@arg_digest()
def get_acceptor_atoms(
    molecular_system,
    selection="all",
    inclusion_rules=None,
    exclusion_rules=None,
    default_inclusion_rules=True,
    default_exclusion_rules=True,
    syntax="MolSysMT",
):
    """
    Identifying acceptor atoms within a molecular system for hydrogen-bond detection.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    inclusion_rules : str, list of str, tuple of str, or None, default=None
        Additional atom-selection rules in `syntax` identifying acceptor atoms.
        Caller-owned rule lists are not modified.
    exclusion_rules : str, list of str, tuple of str, or None, default=None
        Additional atom-selection rules in `syntax` excluding acceptor atoms.
        Caller-owned rule lists are not modified.
    default_inclusion_rules : bool, default=True
        Whether to apply default chemical inclusion rules.
    default_exclusion_rules : bool, default=True
        Whether to apply default chemical exclusion rules.
    syntax : str, default='MolSysMT'
        Selection syntax for `selection` and custom rules. Built-in default
        rules always use MolSysMT syntax, independently of this argument.

    Returns
    -------
    numpy.ndarray
        Sorted int64 array of source acceptor atom indices, with shape ``(n,)``.
        A valid no-match query returns shape ``(0,)`` with the same integer dtype.

    Raises
    ------
    ArgumentError
        If the declared syntax, selection or a custom rule is invalid.

    Notes
    -----
    Rules inspect the supplied atom types, names, groups and covalent bonds.
    A rule with no matching atoms is a valid empty selection. Hydrogen-free
    inputs may contain acceptor candidates but no explicit donor-hydrogen
    pairs; this operation does not reconstruct hydrogens.

    Examples
    --------
    >>> import molsysmt as msm
    >>> builder = msm.MolSysBuilder()
    >>> _ = builder.add_atom(atom_name='O', atom_type='O')
    >>> _ = builder.add_group([0], group_name='LIG')
    >>> rules = ["atom_type=='O'"]
    >>> msm.interactions.hbonds.get_acceptor_atoms(
    ...     builder.build(), inclusion_rules=rules).tolist()
    [0]
    >>> rules
    ["atom_type=='O'"]

    .. admonition:: User guide

       See :ref:`Tutorial_Get_acceptor_atoms` for customizing acceptor rules.

    .. versionadded:: 1.0.0
    """

    from ._role_rules import select_role_atoms

    output = select_role_atoms(
        molecular_system,
        selection,
        syntax,
        inclusion_rules,
        exclusion_rules,
        acceptor_inclusion_rules if default_inclusion_rules else (),
        acceptor_exclusion_rules if default_exclusion_rules else (),
    )
    return np.asarray(sorted(output), dtype=np.int64)
