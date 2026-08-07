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
        Input system in any supported form.
    element : {'group'}, default 'group'
        Hierarchical element for which transmembrane tendency is returned.
        Only ``'group'`` (residue level) is currently supported.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of groups to include in the output.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    definition : {'zhao', 'senes'}, default 'zhao'
        Transmembrane tendency scale to use.

        * ``'zhao'``: free-energy-based scale from Zhao & London (2006).
        * ``'senes'``: pseudo-potential scale from Senes et al. (2007).
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

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
        output.append(group_table_value(values, ii))

    return output

