"""Constructing explicitly declared peptide templates without generating geometry."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "physchem", "preparation"])
@arg_digest()
def get_peptide_chemical_template(
    residue_names,
    n_terminal_state,
    c_terminal_state,
    skip_digestion=False,
    *,
    disulfide_group_pairs=None,
):
    """Constructing a heavy-atom peptide template with explicit chemical states.

    Parameters
    ----------
    residue_names : list, tuple or numpy.ndarray
        Ordered residue-state names, one per zero-based template group index.
        Names are exact and case-sensitive. HIS requires HID, HIE or HIP; ASP/ASH,
        GLU/GLH, LYS/LYN and CYS/CYM/CYX distinguish declared protonation or links.
        No aliases, pH rules or states are inferred from coordinates.
    n_terminal_state : {'ammonium', 'amine'}
        Explicit charged or neutral amino terminus. Proline uses the corresponding
        secondary amine inventory. No terminal state is chosen by default.
    c_terminal_state : {'carboxylate', 'carboxylic_acid'}
        Explicit charged or protonated carboxyl terminus, including an OXT atom.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    disulfide_group_pairs : list, tuple, numpy.ndarray or None, default=None
        Keyword-only integer array of shape (n_disulfides, 2), containing template
        group indices. Every CYX must occur in exactly one pair; other states
        cannot participate. None declares no disulfides. These are chemical bonds,
        not geometric candidates inferred from sulfur proximity.

    Returns
    -------
    dict
        Coordinate-free native MolSys under template, its detached
        template_provenance, and a molsysmt.peptide_template@1 report. The selected
        fragments, terminal states, declared links, source snapshot/digests,
        curation and original executed software are retained. Formal charge uses
        elementary charge units. H counts are stored; no indexed H atoms exist.

    Raises
    ------
    ArgumentError
        If states are unsupported, indices invalid, or disulfide ports unpaired.
    StructuralInconsistencyError
        If the bundled fragment schema or declared formal-charge unit is invalid.

    Notes
    -----
    Experimental template factory for one linear peptide, optionally with declared
    disulfides. This is not an operation on an existing molecular system. Apply
    its result to any supported source form with apply_chemical_template and an
    exhaustive caller-declared atom map. Missing heavy atoms, capped/cyclic or
    modified backbones and arbitrary inter-group links remain outside this factory.
    Terminal OXT is part of the template; an absent source OXT needs separate repair.

    Bundled fragments are curated from a pinned Meeko data snapshot. Meeko and
    RDKit are not runtime dependencies. No conformer, atom matching, protonation
    prediction or force-field parameters are generated. Stereochemistry remains
    unspecified, including peptide cis/trans and residue enantiomers; this is
    not a declaration of L stereochemistry. Existing conflicting source chemistry
    is never overwritten by template application. Keep provenance/report as
    workflow sidecars: H5MSM stores the chemical values, not these sidecars.

    Successful construction contributes portable MolSysMT software and source-data
    attribution to an optional Ackredit scope; it does not credit Meeko/RDKit as
    executed runtime engines. Attribution absence/failure preserves the result.

    See Also
    --------
    assess_chemical_template : Check chemistry and the explicit atom map.
    apply_chemical_template : Transfer compatible chemistry while preserving pose.
    molsysmt.build.add_missing_hydrogens : Generate H geometry in a separate step.

    Examples
    --------
    >>> import molsysmt as msm
    >>> result = msm.physchem.get_peptide_chemical_template(
    ...     ['GLY', 'GLY'], n_terminal_state='ammonium',
    ...     c_terminal_state='carboxylate')
    >>> result['template'].get_n_atoms()
    9
    >>> result['report']['n_stored_hydrogens']
    8

    .. admonition:: Tutorial
       :class: dropdown

       See the chemical-template tutorial in the User Guide.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.peptide_chemical_template import assemble

    return assemble(
        residue_names,
        n_terminal_state,
        c_terminal_state,
        disulfide_group_pairs,
        "molsysmt.physchem.get_peptide_chemical_template",
    )
