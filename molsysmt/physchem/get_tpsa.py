"""Calculating topological polar surface area on complete molecular graphs."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
def get_tpsa(
    molecular_system,
    element="molecule",
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="ertl_rohde_selzer",
    include_sulfur_phosphorus=False,
    return_report=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Calculating Ertl molecular TPSA and selected atomic contribution sums.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form supplying complete chemistry,
        element symbols, hydrogen inventory and molecular membership.
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
        No structure axis is added to these graph-derived outputs.
    chemical_state : str or int, default='reference'
        Chemical state supplying charges, bonds and hydrogen counts. 'structure'
        must resolve to one state across the requested structures.
    method : str, default='ertl_rohde_selzer'
        Ertl, Rohde and Selzer (2000), executed through RDKit. No fallback runs.
    include_sulfur_phosphorus : bool, default=False
        Include polar S/P contributions in addition to N/O when True. False
        follows the conventional N/O-only RDKit/reference-program variant.
    return_report : bool, default=False
        Return a dictionary containing tpsa and a detached provenance report.
    syntax : str, default='MolSysMT'
        Selection syntax. External languages require their optional provider.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated arguments.

    Returns
    -------
    quantity or dict
        Area quantity with shape (n_selected_elements,), standardized through
        PyUnitWizard (nm² by default). 'system' returns a scalar, including zero
        for an empty atom selection; other empty selections retain shape (0,).
        With return_report=True, keys are tpsa and report; the report retains
        source molecule/atom indices, state, method, parameters and attribution.

    Raises
    ------
    ArgumentChoiceError
        If element requests an unsupported level, such as bond.
    ArgumentError
        If method, selections, state or other arguments are invalid.
    StructuralInconsistencyError
        If required chemistry is missing or contradictory, a selected molecule
        is disconnected, a bond crosses its boundary, or chemistry is outside
        the supported closed-shell organic profile.
    ImportError
        If the explicitly required optional RDKit provider is unavailable.

    Notes
    -----
    TPSA is a fitted topological descriptor, not geometric SASA, an observed
    conformation's exposed polar area or a permeability prediction. The original
    fragment contributions are in angstrom². N/O-only and N/O/S/P definitions
    differ; neither is universally superior. Charged graphs are allowed when
    supported by the model; protonation and tautomer states are never prepared.

    Complete closed-shell H/B/C/N/O/F/Si/P/S/Cl/Se/Br/Te/I graphs are admitted.
    Query/dummy atoms, metals, radicals and dative relationships are excluded.
    Declared indexed and nonindexed hydrogen counts must be available and
    preserved; missing counts are not guessed. Aromaticity is checked using
    the general aromaticity tool on detached selected chemistry. The input's
    atoms, assignments, coordinates and provider caches remain unchanged.

    Molecule membership belongs to the source topology; other chemical states
    cannot silently repartition it. Disconnected salt labels and covalent
    adducts crossing a context molecule boundary fail. Several independent
    selected molecules produce separate values. Other levels sum contributions
    evaluated on complete parent molecules; no cut fragment is recalculated.
    These sums describe model contributions, not exposed physical area.
    Optional Ackredit credits the original model and actual executed software;
    completed empty selections retain provenance. Default quantity outputs
    carry no report; request return_report=True to retain scientific provenance.

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
    molsysmt.physchem.get_sasa : Calculating geometric solvent-accessible areas.
    molsysmt.physchem.get_aromaticity : Checking state-specific aromaticity.
    molsysmt.chemical_states.get_covalent_blocks : Finding covalently connected blocks.

    References
    ----------
    Ertl, P., Rohde, B. and Selzer, P. (2000). Fast Calculation of Molecular
    Polar Surface Area as a Sum of Fragment-Based Contributions and Its
    Application to the Prediction of Drug Transport Properties. Journal of
    Medicinal Chemistry 43, 3714–3717. doi:10.1021/jm000942e.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> area = msm.physchem.get_tpsa(Chem.MolFromSmiles('CCO'))
    >>> msm.pyunitwizard.get_value(area, to_unit='angstrom**2').round(2).tolist()
    [20.23]

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_tpsa` for molecules, chemical states and units.

    .. versionadded:: 1.0.0
    """
    from molsysmt import pyunitwizard as puw

    from ._molecular_descriptors import calculate_molecular_descriptor

    caller = "molsysmt.physchem.get_tpsa"
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
        descriptor="tpsa",
        method=method,
        article_key="ertl_2000",
        caller=caller,
        return_report=return_report,
        parameters=dict(
            include_sulfur_phosphorus=include_sulfur_phosphorus,
            hydrogen_treatment="preserve_declared_inventory",
            implementation="rdkit.CalcTPSA",
        ),
    )
    result = puw.quantity(values, "angstrom**2", standardized=True)
    return dict(tpsa=result, report=report) if return_report else result
