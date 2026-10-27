from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    ArgumentError,
    NotImplementedMethodError,
)
from molsysmt.physchem.groups._lookup import group_table_value


@arg_digest()
def get_bulkiness(
    molecular_system,
    element="group",
    selection="all",
    definition="zimmerman",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting Zimmerman reference bulkiness areas for amino-acid groups.

    Look up side-chain reference descriptors by group name without geometric
    calculations. The area interpretation follows Proust et al. (2019), Table 1.
    This experimental tool does not measure the input conformation's surface.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT form supplying group names.
    element : str, default='group'
        Only 'group' is supported. Other levels fail before resolving selection;
        no molecular area or sequence average is inferred.
    selection : str, int, list, tuple, or numpy.ndarray, default='all'
        Selection of groups. Numeric indices preserve order and repetitions;
        strings are evaluated using the requested syntax.
    definition : str, default='zimmerman'
        Published reference scale. Only 'zimmerman' is supported.
    syntax : str, default='MolSysMT'
        Selection syntax. External languages require their optional provider.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated arguments.

    Returns
    -------
    quantity
        Floating area values with shape (n_groups,), standardized through
        PyUnitWizard (nm² with the default policy). Explicit angstrom² extraction
        retains the tabulated numbers, including ALA 11.5 and GLY 3.4. Empty
        selections return a typed zero-length area quantity.

    Raises
    ------
    ArgumentChoiceError
        If element requests an unsupported population level.
    UnknownGroupInTableError
        If a selected name is absent from the twenty standard amino-acid
        entries, including modified groups, terminal caps and DUM/X placeholders.
    ArgumentError
        If group names are missing, or definition, selection or another
        digested argument is invalid.

    Notes
    -----
    The unchanged table matches AAindex1 ZIMJ680102 and official ProtScale.
    These curations establish numeric compatibility; neither inspected entry
    explicitly declares units. Proust et al. report the Zimmerman descriptor
    as side-chain section in angstrom². The original 1968 full-text derivation
    and normalization have not been independently audited here.

    Group identities suffice: no chemical-state preparation, hydrogen placement,
    force field, structure index or periodic geometry is inferred. A name match
    is not a chemical validation of the actual group. Unsupported names receive
    neither an inferred parent value nor zero area. Use explicit group indices
    to exclude unsupported groups such as terminal caps. Summing these reference
    values does not yield a molecule's physical area. Only group names are requested; coordinates and chemical assignments are
    unchanged. Optional Ackredit tracking credits the reference scale and later
    area interpretation once per completed call, including an empty selection;
    it does not claim to execute ProtScale or the original generation procedure.

    See Also
    --------
    molsysmt.physchem.get_volume : Getting tabulated volume descriptors.
    molsysmt.physchem.get_sasa : Calculating coordinate-based solvent exposure.

    References
    ----------
    Zimmerman, J. M., Eliezer, N. and Simha, R. (1968). The characterization of
    amino acid sequences in proteins by statistical methods. Journal of
    Theoretical Biology 21, 170-201. doi:10.1016/0022-5193(68)90069-6.

    Proust, L. et al. (2019). Insights Into the Complexity of Yeast Extract
    Peptides and Their Utilization by Streptococcus thermophilus. Frontiers in
    Microbiology 10, 906. doi:10.3389/fmicb.2019.00906, Table 1.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> area = msm.physchem.get_bulkiness(molsys, selection=[1, 2])
    >>> msm.pyunitwizard.get_value(area, to_unit='angstrom**2').round(2).tolist()
    [11.5, 11.5]

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_bulkiness` for units, selections and limitations.

    .. versionadded:: 1.0.0
    """
    from molsysmt.basic import get

    from .groups.bulkiness import units, zimmerman

    caller = "molsysmt.physchem.get_bulkiness"
    if element != "group":
        raise ArgumentChoiceError(
            argument="element", value=element, choices=["group"], caller=caller
        )
    if definition != "zimmerman":
        raise NotImplementedMethodError(caller=caller)
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
    values = [
        group_table_value(
            zimmerman,
            name,
            table="Zimmerman bulkiness",
            caller=caller,
            allow_placeholders=False,
        )
        for name in names
    ]
    result = puw.standardize(puw.quantity(values, units))

    from molsysmt import _ackredit
    from molsysmt._private.scientific_citations import ARTICLES

    items = [
        dict(
            id="zimmerman_1968",
            type="article",
            **ARTICLES["zimmerman_1968"],
            roles=["reference_scale"],
        ),
        dict(
            id="proust_2019",
            type="article",
            **ARTICLES["proust_2019"],
            roles=["unit_interpretation"],
        ),
    ]
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller, contextual=True)
    return result
