from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError, NotImplementedMethodError
from molsysmt.physchem.groups._lookup import group_table_value


@arg_digest()
def get_surface_area(
    molecular_system,
    element="group",
    selection="all",
    syntax="MolSysMT",
    definition="collantes",
    skip_digestion=False,
):
    """
    Getting standard surface area values for elements in a molecular system.


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
    definition : str, default='collantes'
        Identifier of the published reference table to query.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list
        Raw Collantes reference descriptor values, one per selected group.
        The physical unit/normalization is under review in issue #473; no
        quantity conversion or conformational SASA measurement is performed.


    Raises
    ------
    ArgumentChoiceError
        If element requests an unsupported population level.
    NotImplementedMethodError
        If definition is not supported.

    Notes
    -----
    Numeric group indices retain order and repetitions. Empty selections
    return the same container with length zero. The existing reference table
    and numerical values are unchanged; this query does not calculate a
    conformational geometric surface or volume, prepare chemistry or assign
    a chemical state. Unknown non-placeholder groups retain explicit errors.
    String selections use the requested syntax. Optional selection languages
    require their provider; the ordinary default remains MolSysMT.
    Unsupported element levels fail before selection is interpreted.
    The Collantes descriptor's physical unit/normalization remains under
    review in uibcdf/molsysmt#473. Raw values are retained without guessed
    conversion or a new physical-unit guarantee.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> result = msm.physchem.get_surface_area(molsys, element='group', selection=[3, 1, 3])
    >>> len(result)
    3

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_surface_area` for reference values and selections.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if element != "group":
        raise ArgumentChoiceError(
            argument="element",
            value=element,
            choices=["group"],
            caller="molsysmt.physchem.get_surface_area",
        )

    if definition == "collantes":
        from .groups.surface_area import collantes as values
    else:
        raise NotImplementedMethodError

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
                table="surface area",
                caller="molsysmt.physchem.get_surface_area",
            )
        )

    return output
