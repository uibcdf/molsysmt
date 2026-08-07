from molsysmt._private.argdigest import arg_digest
from molsysmt.physchem.groups._lookup import group_table_value
from molsysmt._private.smonitor import NotImplementedMethodError

@arg_digest()
def get_polarity(molecular_system, element='group', selection = 'all', syntax='MolSysMT', definition='grantham',
                 skip_digestion=False):
    """
    Polarity index per residue group from a reference scale.

    Returns a dimensionless polarity value for each selected residue group,
    looked up from one of the published amino-acid polarity scales.  Polarity
    quantifies the tendency of the side chain to participate in electrostatic
    interactions and hydrogen bonding.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    element : {'group'}, default 'group'
        Hierarchical element for which polarity is returned.  Only ``'group'``
        (residue level) is currently supported.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of groups to include in the output.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    definition : {'grantham', 'zimmerman'}, default 'grantham'
        Polarity scale to use.

        * ``'grantham'``: side-chain polarity from Grantham (1974), used in
          the original amino acid distance metric.
        * ``'zimmerman'``: polarity scale from Zimmerman et al. (1968).
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

    Returns
    -------
    list of float
        Polarity values for each selected group, in the same order as the
        selection.  Length ``n_groups``.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.

    Notes
    -----
    Supported scales and their primary references:

    * ``'grantham'``: Grantham R. *Science* 185:862–864 (1974).
    * ``'zimmerman'``: Zimmerman J.M., Eliezer N., Simha R.
      *J. Theor. Biol.* 21:170–201 (1968).

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if definition == 'grantham':
        from molsysmt.physchem.groups.polarity import grantham as values
    elif definition == 'zimmerman':
        from molsysmt.physchem.groups.polarity import zimmerman as values
    else:
        raise NotImplementedMethodError()

    group_names = get(molecular_system, element='group', selection=selection, syntax=syntax, group_name=True)

    output = []

    for ii in group_names:
        output.append(group_table_value(values, ii))

    return output

