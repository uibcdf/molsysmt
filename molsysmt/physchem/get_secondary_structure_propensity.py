import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError
from molsysmt.physchem.groups._lookup import group_table_value


@arg_digest()
def get_secondary_structure_propensity(
    molecular_system,
    conformation,
    element="group",
    selection="all",
    definition="levitt_1978_weighted",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting reference secondary-structure propensities for amino-acid groups.

    Look up the weighted relative frequencies of Levitt (1978), Tables III–V,
    by group name. This experimental tool neither predicts secondary structure
    from sequence nor assigns it from coordinates.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT form supplying group names.
    conformation : str
        Reference category: 'alpha_helix', 'beta_sheet' or 'reverse_turn'.
        Required; no category is inferred from the input coordinates.
    element : str, default='group'
        Only 'group' is supported. Other levels fail before resolving selection.
    selection : str, int, list, tuple, or numpy.ndarray, default='all'
        Selection of groups. Numeric indices preserve order and repetitions;
        strings are evaluated using the requested syntax.
    definition : str, default='levitt_1978_weighted'
        Published scale variant. Only 'levitt_1978_weighted' is supported.
    syntax : str, default='MolSysMT'
        Selection syntax. External languages require their optional provider.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated arguments.

    Returns
    -------
    numpy.ndarray
        Detached float64 array of dimensionless frequency ratios with shape
        (n_groups,). An empty selection returns shape (0,). Values may exceed
        one; they are not probabilities and are independent of unit policy.

    Raises
    ------
    ArgumentChoiceError
        If element requests an unsupported population level.
    UnknownGroupInTableError
        If a selected name is absent from the twenty standard amino-acid
        entries, including modified groups, terminal caps and DUM/X placeholders.
    ArgumentError
        If conformation, definition, selection or another digested argument is
        invalid, or selected group names are missing.

    Notes
    -----
    The existing tables match the P_ij columns of Levitt's detailed Tables III,
    IV and V, and AAindex1 LEVM780101–103. The reverse-turn vector follows
    Table V rather than the differing summary Table II. The reference ratio is
    P_ij = (n_ij/N_i)/(N_j/N_t), using the paper's weighted population counts.
    One denotes the reference expectation. The three category values need not
    sum to one. No clipping, renormalization, averaging or class assignment is
    performed. The values are reference descriptors, not measured properties
    of the input conformation. No implicit coil remainder is defined.

    Group names suffice; no coordinates, chemical-state assignment, periodic
    geometry or sequence window is used. Unsupported names receive neither a
    parent-amino-acid substitution nor a zero. Optional Ackredit credits the
    reference data once per completed lookup, including empty selections; it
    does not claim execution of the original table-generation procedure.

    See Also
    --------
    molsysmt.structure.get_secondary_structure : Assigning observed secondary structure.
    molsysmt.physchem.get_bulkiness : Getting reference side-chain bulkiness areas.

    References
    ----------
    Levitt, M. (1978). Conformational preferences of amino acids in globular
    proteins. Biochemistry 17, 4277–4285. doi:10.1021/bi00613a026, Tables III–V.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> msm.physchem.get_secondary_structure_propensity(
    ...     molsys, 'alpha_helix', selection=[1, 2]).tolist()
    [1.29, 1.29]

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_secondary_structure_propensity` for categories,
       selections and the distinction from observed secondary structure.

    .. versionadded:: 1.0.0
    """
    from molsysmt.basic import get

    from .groups import secondary_structure_propensity as tables

    caller = "molsysmt.physchem.get_secondary_structure_propensity"
    if element != "group":
        raise ArgumentChoiceError(
            argument="element", value=element, choices=["group"], caller=caller
        )
    if definition != "levitt_1978_weighted":
        raise ArgumentError("definition", value=definition, caller=caller)
    definitions = {
        "alpha_helix": tables.alpha_helix_levitt,
        "beta_sheet": tables.beta_sheet_levitt,
        "reverse_turn": tables.beta_turn_levitt,
    }
    if not isinstance(conformation, str) or conformation not in definitions:
        raise ArgumentError("conformation", value=conformation, caller=caller)
    names = get(
        molecular_system,
        element="group",
        selection=selection,
        syntax=syntax,
        group_name=True,
    )
    if names is None or any(not isinstance(name, str) for name in names):
        raise ArgumentError(
            argument="molecular_system",
            caller=caller,
            message="The molecular system must provide names for every selected group.",
        )
    result = np.array(
        [
            group_table_value(
                definitions[conformation],
                name,
                table=f"Levitt 1978 weighted {conformation}",
                caller=caller,
                allow_placeholders=False,
            )
            for name in names
        ],
        dtype=np.float64,
    )

    from molsysmt import _ackredit
    from molsysmt._private.scientific_citations import ARTICLES

    items = [
        dict(
            id="levitt_1978",
            type="article",
            **ARTICLES["levitt_1978"],
            roles=["reference_scale"],
        )
    ]
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller, contextual=True)
    return result
