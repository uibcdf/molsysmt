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
    context_atom_correspondence=None,
):
    """Assessing chemical compatibility through an exhaustive declared atom map.

    Parameters
    ----------
    molecular_system : molecular system
        Source in any supported form providing elements and stored relationships.
        Without context, requires one isolated connected component. Explicit template
        completion can assess disconnected fragments of that same mapped component.
    template : molecular system
        Explicitly prepared template in any supported form. Coordinates are not
        required. Its selected state must declare complete covalent connectivity,
        formal charges, aromatic flags, radical and hydrogen-count assignments.
    atom_correspondence : list, tuple or numpy.ndarray
        Exhaustive bijection of shape (n_selected_atoms, 2): template indices followed by
        full source indices, both zero-based. Covers every selected source atom
        and every template atom, including explicit hydrogens.
        With context_atom_correspondence, covers the selected source atoms and
        their corresponding template atoms; other template atoms need not be mapped.
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
        Selected completion preserves unrelated component memberships/labels.
        Context transfer supports only require_same_graph in this version.

    selection : str, list, tuple or numpy.ndarray, default='all'
        One full stored component, or a nonempty atom scope with explicit
        context_atom_correspondence. Strings use topological
        selections. The template map covers precisely these atoms, using indices
        in the full source input. Without context, external relationships stay unassessed.
    syntax : str, default='MolSysMT'
        Selection syntax used to select source atoms.
    context_atom_correspondence : list, tuple, numpy.ndarray or None, default=None
        Optional keyword-only bijection (n_context_atoms, 2), template indices
        then source indices. Disjoint from atom_correspondence in both axes.
        Declares external context for selected atoms in a larger complete
        template; every selected atom's source/reference neighbors and bond
        stereo references must be mapped. Context atoms are checked for element,
        isotope and existing chemical conflicts, but receive no assignments.
        None retains the exhaustive closed-component contract. An empty int64
        array of shape (0, 2) explicitly requests context mode without neighbors.

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
    Without an explicit context map, a selected component must have no stored
    relationship to external atoms.
    Unrelated components remain outside the assessment; global completeness is
    not elevated by a successful selected-component application. The report
    records full-source indices and the assessed scope. All coordinates remain
    untouched; coordinate-dependent selections are not supported.
    Selected edge completion also checks that rebuilding will preserve unrelated
    component memberships; an inconsistent outside partition stays unassessed.
    Explicit context mode permits disconnected selections and transfers only
    selected atom fields and all incident bond fields, including boundary bonds.
    Outside atom fields and outside-only bonds remain untouched. Missing context,
    unsupported links or mismatched incident edges prevent application; no
    cut termini, missing bond or protonation state is inferred. Unmapped template
    atoms remain outside assessment. Scoped evidence does not elevate global
    connectivity or make full-graph recognizers accept an unprepared polymer.

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
        context_atom_correspondence,
    )[0]
