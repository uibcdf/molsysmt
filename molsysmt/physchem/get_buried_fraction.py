from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError, NotImplementedMethodError
from molsysmt.physchem.groups._lookup import group_table_value


@arg_digest()
def get_buried_fraction(
    molecular_system,
    element="group",
    selection="all",
    definition="janin",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting Janin reference buried-fraction descriptors for selected groups.

    Returns a tabulated molar fraction value representing how frequently each
    residue type is found in a buried (solvent-inaccessible) environment in a
    reference dataset of folded proteins.  Values are looked up from a static
    scale indexed by residue name.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='group'
        Only 'group' is supported. Other levels raise ArgumentChoiceError
        before resolving selection; no aggregate is inferred.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    definition : str, default='janin'
        Identifier of the published reference table to query.
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
    ArgumentChoiceError
        If element requests an unsupported population level.
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.


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

    The ``'janin'`` scale reports the molar fraction (%) of each amino acid
    among 2001 buried residues from a structural database, as described in:

        Janin J. *Nature* 277:491–492 (1979).


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> result = msm.physchem.get_buried_fraction(molsys, element='group', selection=[3, 1, 3])
    >>> len(result)
    3

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_buried_fraction` for reference values and selections.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if element != "group":
        raise ArgumentChoiceError(
            argument="element",
            value=element,
            choices=["group"],
            caller="molsysmt.physchem.get_buried_fraction",
        )

    if definition == "janin":
        from .groups.buried_fraction import janin as values
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
                table="buried fraction",
                caller="molsysmt.physchem.get_buried_fraction",
            )
        )

    return output
