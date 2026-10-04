"""Assessing explicitly mapped chemical templates before preparation."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "physchem", "preparation"])
@arg_digest()
def assess_chemical_template(
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
    """Assessing chemical compatibility through an exhaustive declared atom map.

    Parameters
    ----------
    molecular_system : molecular system
        Source in any supported form providing elements and stored relationships.
        The default requires one isolated connected component. Explicit template
        completion can assess disconnected fragments of that same mapped component.
    template : molecular system
        Explicitly prepared template in any supported form. Coordinates are not
        required. Its selected state must declare complete covalent connectivity,
        formal charges, aromatic flags, radical and hydrogen-count assignments.
    atom_correspondence : list, tuple or numpy.ndarray
        Exhaustive bijection of shape (n_selected_atoms, 2): template indices followed by
        full source indices, both zero-based. Covers every selected source atom
        and every template atom, including explicit hydrogens.
    template_provenance : dict
        JSON-compatible declaration with nonempty identity, version, source_uri,
        checksum and hydrogen_policy strings. Policy is 'explicit_atoms' for zero
        stored virtual H counts or 'stored_counts' for an explicitly different
        template policy. Identity/checksum are declarations, not authentication.
    chemical_state : str, int or None, default='reference'
        Source state index or resolved reference. Ambiguity remains unassessed.
        'structure' is unavailable in this coordinate-independent operation.
    template_chemical_state : str, int or None, default='reference'
        Independent template state index or resolved reference.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    connectivity_policy : {'require_same_graph', 'complete_from_template'}, default='require_same_graph'
        Keyword-only policy. The default requires identical stored atom pairs.
        Explicit completion proposes missing template bonds in an incomplete
        source graph. Unexpected edges, declared complete-graph differences and
        conflicting assignments fail; no stored edge is removed or overwritten.
        Missing bonds on a proper source subset remain unassessed; complete an
        extracted component explicitly.

    selection : str, list, tuple or numpy.ndarray, default='all'
        One full stored component to assess or update. Strings use topological
        selections. The template map covers precisely these atoms, using indices
        in the full source input. Stored external relationships stay unassessed.
    syntax : str, default='MolSysMT'
        Selection syntax used to select source atoms.

    Returns
    -------
    dict
        Detached molsysmt.chemical_template@1 report with compatible, conflict
        or unassessed status, original states/map, proposed absent-field
        assignments, preserved explicit fields, indexed issues, template
        provenance and producer versions. Formal charges use elementary charge.
        Unsupported or unnormalized chemistry cannot become compatible.

    Raises
    ------
    ArgumentError
        If the map/provenance is malformed, nonexhaustive or outside either axis.
    StructuralInconsistencyError
        If native domains or an explicit state index are invalid.
    FormatError
        If a source form adapter rejects an unsupported encoding.

    Notes
    -----
    Neither input is changed. Elements/isotopes, stored graph and explicit fields
    must agree. Missing fields can be proposed. Only explicit template completion
    can propose absent edges, with original template bond indices and source pairs
    in added_bonds. The exhaustive template must remain one connected component.
    Aromatic or stereo-reference encodings needing normalization stay unassessed;
    no equivalent chemical state is inferred. This is correspondence checking,
    not template validation, protonation selection, hydrogen placement or docking
    certification. Unknown template fields cannot authorize a source overwrite.
    A selected component must have no stored relationship to external atoms.
    Unrelated components remain outside the assessment; global completeness is
    not elevated by a successful selected-component application. The report
    records full-source indices and the assessed scope. All coordinates remain
    untouched; coordinate-dependent selections are not supported.

    See Also
    --------
    apply_chemical_template : Apply the same preflight transactionally on a copy.
    get_chemical_readiness : Inspect stored chemical fields.

    Examples
    --------
    >>> import numpy as np
    >>> import molsysmt as msm
    >>> molsys = msm.systems['caffeine']['caffeine.sdf']
    >>> provenance = dict(identity='bundled caffeine', version='fixture',
    ...     source_uri='bundled:caffeine.sdf', checksum='caller-declared fixture',
    ...     hydrogen_policy='explicit_atoms')
    >>> report = msm.physchem.assess_chemical_template(molsys, template=molsys,
    ...     atom_correspondence=np.column_stack((np.arange(24), np.arange(24))),
    ...     template_provenance=provenance)
    >>> report['status']  # Native CTAB reading does not invent all template fields.
    'unassessed'

    .. admonition:: User guide

       See :ref:`Tutorial_Chemical_Templates` for the preparation contract.

    .. versionadded:: 1.0.0
    """
    # Compatibility with the truthy bypass in ArgDigest 0.13.0 (#17).
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(
            skip_digestion, caller="molsysmt.physchem.assess_chemical_template"
        )
    from molsysmt._private.chemical_template import evaluate

    return evaluate(
        molecular_system,
        template,
        atom_correspondence,
        template_provenance,
        chemical_state,
        template_chemical_state,
        "molsysmt.physchem.assess_chemical_template",
        connectivity_policy,
        selection,
        syntax,
    )[0]
