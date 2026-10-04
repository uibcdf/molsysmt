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
):
    """Applying compatible declared template assignments to an independent system.

    Parameters
    ----------
    molecular_system : molecular system
        Source in any supported form supplying one mapped component, possibly
        fragmented when explicit template completion is requested. Existing
        atoms, relationships and all coordinate frames are preserved.
    template : molecular system
        Prepared template in a supported form with complete explicit chemical
        assignments and the same atoms. Its coordinates are never transferred.
    atom_correspondence : list, tuple or numpy.ndarray
        Exhaustive bijection of shape (n_atoms, 2), with template and source
        atom indices in the first and second columns. Includes explicit H atoms.
    template_provenance : dict
        Detached JSON-compatible identity, version, source_uri, checksum and
        hydrogen_policy declaration; see assess_chemical_template. Policy is
        'explicit_atoms' or 'stored_counts'. This does not authenticate the data.
    chemical_state : str, int or None, default='reference'
        Source state index or resolved reference to update. Other states remain
        unchanged. 'structure' requires a different frame-based operation.
    template_chemical_state : str, int or None, default='reference'
        Independent template state index or resolved reference.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    connectivity_policy : {'require_same_graph', 'complete_from_template'}, default='require_same_graph'
        Keyword-only choice. Explicit completion adds missing bonds from the
        declared complete template to an incomplete source graph. Default behavior
        still requires identical edges. Conflicts and unexpected source edges fail.

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
    identity/membership, structures, units, box and frame/state associations are
    preserved. State replacement invalidates analyses through the existing native
    lifecycle. Mechanical parameters are copied but are not reparameterized.
    The returned report retains template provenance separately; native/H5MSM
    chemical values do not yet embed that report or a new provenance table.
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
    )
    return apply(molecular_system, report, source, caller)
