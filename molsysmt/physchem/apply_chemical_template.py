"""Applying explicit missing chemical assignments without changing a molecular pose."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "physchem", "preparation"])
@arg_digest()
def apply_chemical_template(
    molecular_system,
    template,
    atom_correspondence,
    template_provenance,
    chemical_state="reference",
    template_chemical_state="reference",
    skip_digestion=False,
    *,
    connectivity_policy="require_same_graph",
    selection="all",
    syntax="MolSysMT",
):
    """Applying compatible declared template assignments to an independent system.

    Parameters
    ----------
    molecular_system : molecular system
        Source in any supported form supplying one selected mapped component, possibly
        fragmented when explicit template completion is requested. Existing
        atoms, relationships and all coordinate structures are preserved.
    template : molecular system
        Prepared template in a supported form with complete explicit chemical
        assignments and the same atoms. Its coordinates are never transferred.
    atom_correspondence : list, tuple or numpy.ndarray
        Exhaustive bijection of shape (n_selected_atoms, 2), with template and source
        atom indices in the first and second columns, in their full input axes.
        Covers every selected source atom and template atom, including explicit H.
    template_provenance : dict
        Detached JSON-compatible identity, version, source_uri, checksum and
        hydrogen_policy declaration; see assess_chemical_template. Policy is
        'explicit_atoms' or 'stored_counts'. This does not authenticate the data.
    chemical_state : str, int or None, default='reference'
        Source state index or resolved reference to update. Other states remain
        unchanged. 'structure' requires a different structure-based operation.
    template_chemical_state : str, int or None, default='reference'
        Independent template state index or resolved reference.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    connectivity_policy : {'require_same_graph', 'complete_from_template'}, default='require_same_graph'
        Keyword-only choice. Explicit completion adds missing bonds from the
        declared complete template to an incomplete source graph. Default behavior
        still requires identical edges within the selection. Conflicts and
        unexpected selected source edges fail. Missing bonds on a proper source
        subset remain unassessed; complete an extracted component explicitly.

    selection : str, list, tuple or numpy.ndarray, default='all'
        One full stored component to assess or update. Strings use topological
        selections. The template map covers precisely these atoms, using indices
        in the full source input. Stored external relationships stay unassessed.
    syntax : str, default='MolSysMT'
        Selection syntax used to select source atoms.

    Returns
    -------
    dict
        molecular_system is a new native MolSys; report is the detached
        molsysmt.chemical_template@1 assessment with status='applied', filled and
        preserved fields, original provenance/software and optional attribution.
        Formal charges use elementary charge units. The report identifies named
        analyses invalidated by chemical-state replacement on the returned copy.
        Added bonds carry template indices, remapped source pairs, user_defined
        evidence and final bond indices; existing bond indices may reorder and are
        mapped by source_bond_correspondence. Components are rebuilt only after
        adding bonds, with new indices/IDs and unknown names/types; group/molecule
        inventory and all other states are preserved.

    Raises
    ------
    ArgumentError
        If a state/map/provenance argument is malformed or nonexhaustive.
    StructuralInconsistencyError
        If preflight is conflict/unassessed. Its report attribute retains the
        detached assessment; neither input is modified.
    FormatError
        If an adapter rejects unsupported source chemical encodings.

    Notes
    -----
    Runs the same preflight as assess_chemical_template before copying or assigning.
    Only absent supported state fields are filled; explicit conflicts fail. No
    atom, isotope, protomer or geometry is generated. The default adds no edge;
    explicit completion transfers missing template edges with declared provenance.
    Connectivity coverage
    is justified by the exhaustive map to the declared complete template; this
    does not independently certify valence or template correctness. Stable atom
    identity/membership, structures, units, box and structure/state associations are
    preserved. State replacement invalidates analyses through the existing native
    lifecycle. Mechanical parameters are copied but are not reparameterized.
    A proper atom subset leaves global connectivity completeness unchanged and
    records scoped evidence in the report; it does not certify unrelated atoms.
    Completing selected bonds can renumber components but retains labels of
    unchanged atom sets. Merged/split sets lose those labels. Unrelated stored
    partitions needing reconciliation remain unassessed during preflight.
    No new atom is inserted and no selected atom is moved.
    The returned report is also retained in the selected ChemicalStates record.
    ``result.chemical_states.get_preparation_history()`` returns independent
    historical envelopes with original operation indices and output dimensions.
    H5MSM 0.5 and ChemicalStatesDict preserve this history. Subsequent edits,
    extraction or merging do not rewrite those indices or certify current chemistry.
    Optional Ackredit absence/failure never changes the scientific outcome.

    See Also
    --------
    assess_chemical_template : Inspect compatibility without modifying inputs.
    molsysmt.build.get_residue_chemical_coverage : Inspect exact residue coverage.

    Examples
    --------
    >>> import numpy as np
    >>> import molsysmt as msm
    >>> molsys = msm.systems['caffeine']['caffeine.sdf']
    >>> provenance = dict(identity='bundled caffeine', version='fixture',
    ...     source_uri='bundled:caffeine.sdf', checksum='caller-declared fixture',
    ...     hydrogen_policy='explicit_atoms')
    >>> try:
    ...     result = msm.physchem.apply_chemical_template(molsys, template=molsys,
    ...         atom_correspondence=np.column_stack((np.arange(24), np.arange(24))),
    ...         template_provenance=provenance)
    ... except msm.StructuralInconsistencyError as error:
    ...     print(error.report['status'])
    unassessed

    .. admonition:: User guide

       See :ref:`Tutorial_Chemical_Templates` for successful mapped applications.

    .. versionadded:: 1.0.0
    """
    caller = "molsysmt.physchem.apply_chemical_template"
    # Compatibility with the truthy bypass in ArgDigest 0.13.0 (#17).
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(skip_digestion, caller=caller)
    from molsysmt._private.chemical_template import apply, evaluate

    report, source, _ = evaluate(
        molecular_system,
        template,
        atom_correspondence,
        template_provenance,
        chemical_state,
        template_chemical_state,
        caller,
        connectivity_policy,
        selection,
        syntax,
    )
    return apply(molecular_system, report, source, caller)
