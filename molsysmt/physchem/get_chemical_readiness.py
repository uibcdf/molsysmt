"""Assessing available molecular chemistry before explicit preparation."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "physchem", "diagnostics"])
@arg_digest()
def get_chemical_readiness(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Assessing stored chemical fields without repairing or completing chemistry.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form providing an atom domain.
        Incomplete chemistry and coordinate-only native inputs are assessable.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atoms to assess. Source indices are deduplicated and sorted. Incident
        bonds include external endpoints; crossing bonds are reported explicitly.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based). Select exactly one when structures exist;
        a source without structures is assessed with missing coordinate data.
    chemical_state : str, int or None, default='reference'
        State to inspect. 'structure' uses the selected frame association.
        An ambiguous reference or absent association is reported as unassessed
        chemistry; an invalid explicit index raises.
    syntax : str, default='MolSysMT'
        Syntax used for atom selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        Detached molsysmt.chemical_readiness@1 report with source atom/bond
        indices, selected state/frame, per-field values and coverage, explicit
        or inferred bond evidence when stored, connectivity boundary/integrity
        checks, explicit H atom indices and unassessed scientific checks.
        Coverage statuses are present, partial, missing, unsupported, conflict
        or empty. Coordinates contain finite-position booleans, assessed in nm;
        formal charges are in elementary charge units. No universal ready flag
        or chemical-validity certificate is returned.

    Raises
    ------
    ArgumentError
        If an atom/frame selection is invalid or selects multiple structures.
    StructuralInconsistencyError
        If a state index, coordinate shape or combined source axes are invalid.
    FormatError
        If a source uses unsupported chemical encodings in its form adapter.

    Notes
    -----
    A stored value does not establish its original interpretation or validation.
    Unknown atom-property origins remain unassessed. Bond evidence is retained
    as declared, without independently validating its truth. Labels missing or
    'unspecified' do not establish achirality. Virtual/implicit H counts are
    distinct from explicit H atoms and their observed coordinates. The audit
    checks conventional covalent multiplicities 1/2/3 or declared aromatic bonds;
    it does not validate valence, perceive aromaticity, choose protonation or
    predict how many H atoms to add. Source domains remain unchanged.
    H5MSM 0.5 numeric selections read chemical layers and one coordinate frame;
    combined layers require declared identity atom-axis correspondence.
    Rich string selections use the existing public selection machinery.

    See Also
    --------
    get_cip_stereochemistry : Analyze stereochemistry with an explicit provider.
    molsysmt.topology.get_rigid_fragments : Partition explicit chemical connectivity.

    Examples
    --------
    >>> import molsysmt as msm
    >>> report = msm.physchem.get_chemical_readiness(msm.systems['caffeine']['caffeine.sdf'])
    >>> report['fields']['formal_charge']['status']
    'present'
    >>> len(report['explicit_hydrogen_atom_indices'])
    10
    >>> 'valence' in report['unassessed_checks']
    True

    .. admonition:: User guide

       See :ref:`Tutorial_Chemical_Readiness` for coverage and scientific limits.

    .. versionadded:: 1.0.0
    """
    # ArgDigest 0.13.0 predates uibcdf/argdigest#17. Retire this compatibility
    # guard once the public runtime floor includes its literal-True bypass fix.
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(
            skip_digestion, caller="molsysmt.physchem.get_chemical_readiness"
        )
    from molsysmt._private.chemical_readiness import assess

    return assess(
        molecular_system,
        selection,
        structure_indices,
        chemical_state,
        syntax,
        "molsysmt.physchem.get_chemical_readiness",
    )
