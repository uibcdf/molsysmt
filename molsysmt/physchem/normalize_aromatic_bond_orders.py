"""Normalizing already declared aromatic bonds without aromaticity perception."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "physchem", "preparation"])
@arg_digest()
def normalize_aromatic_bond_orders(
    molecular_system, chemical_state="reference", skip_digestion=False
):
    """Normalizing declared aromatic bonds to fractional order 1.5 on a copy.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing stored chemical states. Only bonds already
        marked is_aromatic=True are normalized; unknown flags remain unknown.
    chemical_state : str, int or None, default='reference'
        State index or resolved reference to normalize. Other states are retained.
        'structure' is unavailable in this coordinate-independent operation.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        New native molecular_system and detached aromatic_bond_normalization@1
        report. Source bond indices/pairs and original integer/fractional orders
        align with the normalized aromatic bonds. Missing original orders are
        NaN. The output removes their integer orders and sets fractional order
        1.5; bond multiplicities are dimensionless. The report retains producer
        version, changed indices, unassessed flags and invalidated analysis names.

    Raises
    ------
    ArgumentError
        If the chemical-state selector is malformed or uses 'structure'.
    StructuralInconsistencyError
        If the state is unresolved, or a marked aromatic bond has invalid
        endpoints, incompatible orders, a noncovalent kind, known nonaromatic
        atoms, or unsupported bond stereo. Neither input nor outputs are mutated
        before completing validation.

    Notes
    -----
    Experimental representation operation using stored declarations. It does
    not perceive aromaticity, create bonds, choose Kekule assignments or move
    atoms. A declared aromatic bond can carry integer order 1/2, fractional order
    1.5, or no order; other encodings fail. Nonaromatic/unknown bonds and all atom
    assignments, topology, coordinates, units, structure associations and connectivity
    completeness remain unchanged. Unknown atom aromatic flags are not filled.

    Existing integer orders on marked aromatic bonds are deliberately replaced
    as a representation choice, with originals retained in the report. This is
    separate from absent-field-only template transfer. It neither normalizes
    guanidinium/carboxylate resonance nor certifies the declarations or valence.
    Changed chemical payload invalidates named interactions on the returned copy;
    an unchanged result retains them. H5MSM persists normalized values, while the
    original representation report remains a workflow sidecar. Native inputs
    need no RDKit; optional Ackredit absence/failure preserves the result.

    See Also
    --------
    get_aromaticity : Perceive aromaticity under an explicitly selected model.
    assess_chemical_template : Assess compatible declared chemical assignments.
    apply_chemical_template : Transfer missing compatible fields.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.physchem.get_peptide_chemical_template(
    ...     ['PHE'], 'ammonium', 'carboxylate')['template']
    >>> result = msm.physchem.normalize_aromatic_bond_orders(molsys)
    >>> result['report']['bond_indices'].size
    6
    >>> result['report']['status']
    'unchanged'

    .. admonition:: User guide

       See :ref:`Tutorial_Normalize_Aromatic_Bond_Orders` for representation limits.

    .. versionadded:: 1.0.0
    """
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(
            skip_digestion, caller=__name__ + ".normalize_aromatic_bond_orders"
        )
    from molsysmt._private.aromatic_bond_normalization import normalize

    return normalize(
        molecular_system,
        chemical_state,
        "molsysmt.physchem.normalize_aromatic_bond_orders",
    )
