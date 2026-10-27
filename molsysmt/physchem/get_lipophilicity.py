"""Calculating state-preserving molecular lipophilicity model descriptors."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
def get_lipophilicity(
    molecular_system,
    element="molecule",
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="wildman_crippen",
    return_report=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Calculating Wildman–Crippen molecular scores and atomic contribution sums.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form supplying complete chemistry,
        element symbols, declared hydrogen inventory and molecular membership.
    element : str, default='molecule'
        Output level: 'atom', 'group', 'component', 'molecule', 'chain',
        'entity' or 'system'. Molecules return complete descriptors; other
        levels return atomic contributions or their sums in complete context.
    selection : str, int, list, tuple, or numpy.ndarray, default='all'
        Elements to return. Numeric indices address the chosen element and
        preserve order and repetitions. For 'system', they are atom indices
        whose contributions are summed. Strings select whole parent elements
        at grouped levels; selected atoms never define capped fragments.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices for spatial selection and chemical-state resolution.
        The graph-derived result has no structure axis.
    chemical_state : str or int, default='reference'
        State supplying bonds, charges and hydrogen counts. 'structure' must
        resolve to one state across the requested structures.
    method : str, default='wildman_crippen'
        Wildman and Crippen (1999) atomic contribution model, executed through
        RDKit. No alternate model or neutralization runs implicitly.
    return_report : bool, default=False
        Return lipophilicity and a detached report containing source maps,
        state, formal charges, parameters, producer versions and attribution.
    syntax : str, default='MolSysMT'
        Selection syntax. External languages require their optional provider.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated arguments.

    Returns
    -------
    numpy.ndarray, numpy.float64 or dict
        Dimensionless float64 values of shape (n_selected_elements,). 'system'
        returns a scalar, including zero for an empty atom selection. Other
        empty selections retain shape (0,). Negative contributions are allowed.
        With return_report=True, keys are lipophilicity and report. The report
        contains ragged source atom membership and formally charged atom indices,
        including those in net-neutral molecules. Scores are not area quantities
        and do not change with PyUnitWizard's length policy.

    Raises
    ------
    ArgumentChoiceError
        If element requests an unsupported level, such as bond.
    ArgumentError
        If method, selections, state or other arguments are invalid.
    StructuralInconsistencyError
        If chemistry is incomplete or contradictory, a molecule is disconnected,
        a bond crosses its boundary, or the closed-shell profile is unsupported.
    ImportError
        If the optional RDKit provider is unavailable.

    Notes
    -----
    This experimental tool exposes the model score for the supplied graph.
    It does not predict logD, pKa, species populations or a pH-dependent ensemble.
    For an appropriate uncharged species the model is conventionally used as a
    calculated logP estimate; numeric output for an ion or zwitterion is not
    certification of a physical partition coefficient. Net charge zero alone
    does not establish applicability. No neutralization, counterion stripping,
    tautomer selection or chemical-state preparation is performed.

    Complete closed-shell H/B/C/N/O/F/Si/P/S/Cl/Se/Br/Te/I graphs are admitted.
    Metals, radicals, dummy/query atoms and dative relationships are excluded.
    Indexed and nonindexed hydrogen inventories must be declared and preserved;
    undeclared missing hydrogens are never guessed. The provider materializes
    declared hydrogens only on a temporary graph. Aromaticity is checked through
    the general tool on detached chemistry; source assignments, coordinates,
    provider caches and atom indices remain unchanged.

    Source molecule membership is retained across chemical states. Disconnected
    salt labels and bonds crossing selected molecule boundaries fail. Independent
    molecules return separate scores. Other levels sum atomic contributions
    evaluated on complete parent molecules, without recalculating cut fragments.
    A sum spanning molecules is a model-contribution sum, not a mixture logP.
    No coordinates are copied for descriptor calculation. Default arrays carry no provenance; request return_report=True
    when exporting results. The report is not automatically attached to MolSys
    or stored as a new H5MSM analysis. Optional Ackredit records the original
    scientific model separately from the software actually executed.

    For atom-level output, indexed hydrogens retain their own contributions.
    Contributions from nonindexed hydrogens are assigned to their retained
    attachment atom; no new source indices are invented. Consequently individual
    heavy-atom values depend on H presentation, while sums covering the same
    atoms and attached H agree. This is an attribution convention, not a change
    to the original model. Each needed parent molecule is calculated once.

    Reports distinguish output element_indices, element_atom_indices and
    element_atom_offsets from evaluated molecule_indices, atom_indices and
    atom_offsets. The latter describe
    complete calculation contexts, so their rows need not match nonmolecular
    output rows. output_kind distinguishes molecular descriptors from atomic
    contribution sums. State, units and original scientific provenance remain
    explicit; grouped contributions do not assign new chemical properties.

    See Also
    --------
    molsysmt.physchem.get_tpsa : Calculating unit-aware polar surface descriptors.
    molsysmt.physchem.get_hydrophobicity : Reading group reference scales.
    molsysmt.physchem.get_aromaticity : Checking state-specific aromaticity.

    References
    ----------
    Wildman, S. A. and Crippen, G. M. (1999). Prediction of Physicochemical
    Parameters by Atomic Contributions. Journal of Chemical Information and
    Computer Sciences 39, 868–873. doi:10.1021/ci990307l.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> molsys = Chem.MolFromSmiles('c1ccccc1')
    >>> msm.physchem.get_lipophilicity(molsys).round(4).tolist()
    [1.6866]

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_lipophilicity` for states, selections and reports.

    .. versionadded:: 1.0.0
    """
    from ._molecular_descriptors import calculate_molecular_descriptor

    caller = "molsysmt.physchem.get_lipophilicity"
    if element not in {
        "atom",
        "group",
        "component",
        "molecule",
        "chain",
        "entity",
        "system",
    }:
        raise ArgumentChoiceError(
            argument="element",
            value=element,
            choices=[
                "atom",
                "group",
                "component",
                "molecule",
                "chain",
                "entity",
                "system",
            ],
            caller=caller,
        )
    values, report = calculate_molecular_descriptor(
        molecular_system,
        selection,
        structure_indices,
        chemical_state,
        syntax,
        element=element,
        descriptor="lipophilicity",
        method=method,
        article_key="wildman_1999",
        caller=caller,
        return_report=return_report,
        parameters=dict(
            hydrogen_treatment="preserve_declared_inventory",
            implementation="rdkit.CalcCrippenDescriptors",
            include_hydrogen_contributions=True,
            chemical_preparation="none",
        ),
    )
    return dict(lipophilicity=values, report=report) if return_report else values
