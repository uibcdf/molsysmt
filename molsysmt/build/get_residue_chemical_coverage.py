"""Inspecting exact residue-template coverage without preparing chemistry."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "build", "diagnostics"])
@arg_digest()
def get_residue_chemical_coverage(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Assessing stored residue chemistry against exact supported templates.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form providing group membership and
        atom names. Incomplete chemistry is assessable; absent hierarchy raises.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Groups to inspect. Integer values are source group indices. String
        selections select atoms and inspect the whole groups containing them.
        Results are deduplicated and sorted.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based). Select one when structures exist. A source
        without structures is assessed with missing coordinate data.
    chemical_state : str, int or None, default='reference'
        Chemical state to inspect, or 'structure' for its frame association.
        Ambiguous references and absent associations remain unassessed.
    syntax : str, default='MolSysMT'
        Syntax used for group selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        Detached molsysmt.residue_chemical_coverage@1 report. Each selected
        group has assessed/incomplete/unassessed status, reasons, source atom
        indices, template identity, heavy-atom and element comparison, stored
        intra-group covalent coverage, candidate hydrogen inventories and an
        explicit unassessed protonation status. A shared chemical_readiness
        report retains stored fields, evidence and coordinates checked in nm.
        Assessed means the bounded comparison ran, not chemically validated.

    Raises
    ------
    ArgumentError
        If group/frame indices are invalid or multiple structures are selected.
    StructuralInconsistencyError
        If group membership or required source-axis correspondence is invalid.
    NotWithThisFormError
        If the source does not provide a topology/group domain.

    Notes
    -----
    Exact amino-acid database names and curated MSE, SEP, TPO and MLY templates
    are supported. Sequence aliases do not justify parent-template substitution.
    Unexpected names and duplicate names are reported without automatic matching.
    Missing OXT is not assessed without terminal context. Modified templates are
    heavy-only; ambiguous standard hydrogen variants remain unassessed. No pH,
    protonation, valence, repair placement or force-field policy is inferred.
    Reference orders are absent from the legacy amino-acid database; only the
    curated modified templates support order comparison. Inter-group chemistry
    is retained as boundary indices and is not template-validated.
    Numeric H5MSM 0.5 selections read only the chosen coordinate frame; rich
    selections use existing public selection machinery. Sources stay unchanged.

    See Also
    --------
    get_missing_heavy_atoms : Query missing heavy atoms for supported residues.
    molsysmt.physchem.get_chemical_readiness : Inspect stored chemical fields.
    add_missing_heavy_atoms : Repair supported heavy-atom gaps explicitly.

    Examples
    --------
    >>> import molsysmt as msm
    >>> report = msm.build.get_residue_chemical_coverage(
    ...     msm.systems['T4 lysozyme L99A']['181l.pdb'], selection="group_name=='HOH'")
    >>> report['groups'][0]['status']
    'unassessed'
    >>> report['groups'][0]['reason_codes']
    ['no_exact_residue_template']

    .. admonition:: User guide

       See :ref:`Tutorial_Residue_Chemical_Coverage` for comparison limits.

    .. versionadded:: 1.0.0
    """
    # Remove when the public ArgDigest floor includes uibcdf/argdigest#17.
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(
            skip_digestion, caller="molsysmt.build.get_residue_chemical_coverage"
        )
    from molsysmt._private.residue_chemical_coverage import assess

    return assess(
        molecular_system,
        selection,
        structure_indices,
        chemical_state,
        syntax,
        "molsysmt.build.get_residue_chemical_coverage",
    )
