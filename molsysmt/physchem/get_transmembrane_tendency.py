from molsysmt._private.argdigest import arg_digest
from molsysmt.physchem.groups._lookup import group_table_value
from molsysmt._private.smonitor import NotImplementedMethodError

@arg_digest()
def get_transmembrane_tendency(molecular_system, element='group', selection='all', syntax='MolSysMT',
                               definition='zhao', skip_digestion=False):
    """
    Transmembrane tendency index per residue group.

    Returns a dimensionless score representing the propensity of each selected
    residue to reside within a lipid bilayer.  Values are looked up from a
    static scale indexed by residue name.  Positive values indicate
    hydrophobic (membrane-favouring) character; negative values indicate
    preference for aqueous environments.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='group'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    definition : object, default='zhao'
        Argument definition.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of float
        Transmembrane tendency values for each selected group, in the same
        order as the selection.  Length ``n_groups``.


    Raises
    ------
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.


    Notes
    -----
    Supported scales and their primary references:

    * ``'zhao'``: Zhao G., London E. *Protein Sci.* 15:1987–2001 (2006).
    * ``'senes'``: Senes A. et al. *J. Mol. Biol.* 366:436–448 (2007).


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if definition == 'zhao':
        from .groups.transmembrane_tendency import zhao as values
    elif definition == 'senes':
        from .groups.transmembrane_tendency import senes as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, syntax=syntax, group_name=True)

    output = []

    for ii in group_types:
        output.append(group_table_value(values, ii, table='transmembrane tendency', caller='molsysmt.physchem.get_transmembrane_tendency'))

    return output

