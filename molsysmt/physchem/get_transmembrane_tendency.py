from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError, NotImplementedMethodError
from molsysmt.physchem.groups._lookup import group_table_value


@arg_digest()
def get_transmembrane_tendency(
    molecular_system,
    element="group",
    selection="all",
    syntax="MolSysMT",
    definition="zhao",
    skip_digestion=False,
):
    """
    Getting transmembrane tendency scores for selected amino-acid groups.

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
        Only 'group' is supported. Other levels raise ArgumentChoiceError
        before resolving selection; no aggregate is inferred.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    definition : object, default='zhao'
        Published scale used for the selected population.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of float
        Transmembrane tendency values for each selected group, in the same
        order as the selection.  Length ``n_groups``.


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

    * ``'zhao'``: Zhao G., London E. *Protein Sci.* 15:1987–2001 (2006).
    * ``'senes'``: Senes A. et al. *J. Mol. Biol.* 366:436–448 (2007).


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> result = msm.physchem.get_transmembrane_tendency(molsys, element='group', selection=[3, 1, 3])
    >>> len(result)
    3

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_transmembrane_tendency` for selection, supported scope and reference definitions.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if element != "group":
        raise ArgumentChoiceError(
            argument="element",
            value=element,
            choices=["group"],
            caller="molsysmt.physchem.get_transmembrane_tendency",
        )

    if definition == "zhao":
        from .groups.transmembrane_tendency import zhao as values
    elif definition == "senes":
        from .groups.transmembrane_tendency import senes as values
    else:
        raise NotImplementedMethodError()

    group_types = get(
        molecular_system,
        element="group",
        selection=selection,
        syntax=syntax,
        group_name=True,
    )

    output = []

    for ii in group_types:
        output.append(
            group_table_value(
                values,
                ii,
                table="transmembrane tendency",
                caller="molsysmt.physchem.get_transmembrane_tendency",
            )
        )

    return output
