import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError, NotImplementedMethodError
from molsysmt.physchem.groups._lookup import group_table_value


@arg_digest()
def get_area_buried(
    molecular_system,
    element="group",
    selection="all",
    definition="rose",
    skip_digestion=False,
):
    """
    Getting Rose reference buried-area descriptors for selected groups.

    Returns a tabulated value (in Å²) representing the average surface area
    buried when each residue transfers from a standard (extended chain) state
    to the folded protein interior.  Values are looked up from a static scale
    indexed by residue name.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='group'
        Only 'group' is supported. Other levels raise ArgumentChoiceError
        before resolving selection; no aggregate is inferred.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    definition : str, default='rose'
        Identifier of the published reference table to query.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    numpy.ndarray
        1-D array of shape ``(n_groups,)`` with buried area values in Å².


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
    This API has no syntax argument. For another selection language, resolve
    group indices with basic.select and pass the numeric result here.
    Unsupported element levels fail before selection is interpreted.

    The ``'rose'`` scale reports the average area buried on transfer from a
    standard state to the folded protein, as tabulated for the 20 standard
    amino acids in:

        Rose G.D., Geselowitz A.R., Lesser G.J., Lee R.H., Zehfus M.H.
        *Science* 229:834–838 (1985).


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> result = msm.physchem.get_area_buried(molsys, element='group', selection=[3, 1, 3])
    >>> len(result)
    3

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_area_buried` for reference values and selections.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if element != "group":
        raise ArgumentChoiceError(
            argument="element",
            value=element,
            choices=["group"],
            caller="molsysmt.physchem.get_area_buried",
        )

    if definition == "rose":
        from .groups.area_buried import rose as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element="group", selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(
            group_table_value(
                values,
                ii,
                table="area buried",
                caller="molsysmt.physchem.get_area_buried",
            )
        )

    output = np.array(output)

    return output
