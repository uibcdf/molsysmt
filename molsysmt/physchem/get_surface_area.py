from molsysmt import pyunitwizard as puw
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
    Getting tabulated Collantes isotropic surface-area descriptors.


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
    quantity
        Collantes ISA values with shape (n_groups,), standardized through
        PyUnitWizard (nm² under the default length policy). The table is
        provisionally interpreted as angstrom² by maintainer decision; original
        units, normalization and values remain under verification in issue #473.
        This is a reference lookup, not a conformational SASA measurement.


    Raises
    ------
    ArgumentChoiceError
        If element requests an unsupported population level.
    NotImplementedMethodError
        If definition is not supported.

    Notes
    -----
    Numeric group indices retain order and repetitions. Empty selections
    return an area quantity with a zero-length axis. The existing reference table
    and numerical values are unchanged; this query does not calculate a
    conformational geometric surface or volume, prepare chemistry or assign
    a chemical state. Unknown non-placeholder groups retain explicit errors.
    String selections use the requested syntax. Optional selection languages
    require their provider; the ordinary default remains MolSysMT.
    Unsupported element levels fail before selection is interpreted.
    The original table unit/normalization remains under review in
    uibcdf/molsysmt#473. The angstrom² convention is provisional, not a claim
    that the original paper has been verified. Historical numeric table entries
    remain unchanged. For a model expecting those table-scale values, request
    ``puw.get_value(result, to_unit='angstrom**2')`` explicitly. For example,
    62.9 angstrom² and 0.629 nm² represent the same area under this convention.
    The original work describes amino-acid side-chain descriptors derived from
    optimized structures for QSAR; this function does not run its generation
    procedure or compute an area from the input coordinates.


    References
    ----------
    Collantes, E. R. and Dunn, W. J., III (1995). Amino Acid Side Chain
    Descriptors for Quantitative Structure-Activity Relationship Studies of
    Peptide Analogs. Journal of Medicinal Chemistry, 38(14), 2705-2713.
    https://doi.org/10.1021/jm00014a022 (PMID: 7629809).
    The accessible abstract establishes descriptor identity, not the unit or
    normalization of the table reproduced here.

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
        from .groups.surface_area import units
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

    return puw.standardize(puw.quantity(output, units))
