from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt.physchem.groups._lookup import group_table_value

@arg_digest()
def get_buried_fraction(molecular_system, element='group', selection='all', definition='janin', syntax='MolSysMT',
                        skip_digestion=False):
    """
    Fraction of residues observed in a buried environment.

    Returns a tabulated molar fraction value representing how frequently each
    residue type is found in a buried (solvent-inaccessible) environment in a
    reference dataset of folded proteins.  Values are looked up from a static
    scale indexed by residue name.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='group'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    definition : object, default='janin'
        Argument definition.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of float
        Buried fraction values (in %) for each selected group, in the same
        order as the selection.  Length ``n_groups``.


    Raises
    ------
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.


    Notes
    -----
    The ``'janin'`` scale reports the molar fraction (%) of each amino acid
    among 2001 buried residues from a structural database, as described in:

        Janin J. *Nature* 277:491–492 (1979).


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if definition == 'janin':
        from .groups.buried_fraction import janin as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, group_name=True)

    output = []

    for ii in group_types:
        output.append(group_table_value(values, ii, table='buried fraction', caller='molsysmt.physchem.get_buried_fraction'))

    return output

