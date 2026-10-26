from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError, NotImplementedMethodError
from molsysmt.physchem.groups._lookup import group_table_value


@arg_digest()
def get_polarity(
    molecular_system,
    element="group",
    selection="all",
    syntax="MolSysMT",
    definition="grantham",
    skip_digestion=False,
):
    """
    Getting polarity scores for selected amino-acid groups.

    Returns a dimensionless polarity value for each selected residue group,
    looked up from one of the published amino-acid polarity scales.  Polarity
    quantifies the tendency of the side chain to participate in electrostatic
    interactions and hydrogen bonding.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='group'
        Only 'group' is supported. Other levels raise ArgumentChoiceError
        before resolving selection; no aggregate is inferred.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    definition : object, default='grantham'
        Published scale used for the selected population.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of float
        Polarity values for each selected group, in the same order as the
        selection.  Length ``n_groups``.


    Raises
    ------
    ArgumentChoiceError
        If element requests an unsupported population level.
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.


    Notes
    -----
    Selection strings are resolved with the requested syntax on the supported
    atom/group axis. Explicit numeric indices retain order and repetitions;
    an empty supported population returns an empty result of the same type.
    A table lookup does not assign a chemical state or validate a molecule's
    chemistry. Unknown non-placeholder amino-acid groups retain their table
    diagnostics; no missing property is silently invented.

    Supported scales and their primary references:

    * ``'grantham'``: Grantham R. *Science* 185:862–864 (1974).
    * ``'zimmerman'``: Zimmerman J.M., Eliezer N., Simha R.
      *J. Theor. Biol.* 21:170–201 (1968).


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> result = msm.physchem.get_polarity(molsys, element='group', selection=[3, 1, 3])
    >>> len(result)
    3

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_polarity` for selection, supported scope and reference definitions.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if element != "group":
        raise ArgumentChoiceError(
            argument="element",
            value=element,
            choices=["group"],
            caller="molsysmt.physchem.get_polarity",
        )

    if definition == "grantham":
        from molsysmt.physchem.groups.polarity import grantham as values
    elif definition == "zimmerman":
        from molsysmt.physchem.groups.polarity import zimmerman as values
    else:
        raise NotImplementedMethodError()

    group_names = get(
        molecular_system,
        element="group",
        selection=selection,
        syntax=syntax,
        group_name=True,
    )

    output = []

    for ii in group_names:
        output.append(
            group_table_value(
                values, ii, table="polarity", caller="molsysmt.physchem.get_polarity"
            )
        )

    return output
