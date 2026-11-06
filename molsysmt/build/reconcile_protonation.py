from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.protonation import DIGEST_OPTIONS


@arg_digest(**DIGEST_OPTIONS)
def reconcile_protonation(
    molecular_system, pH=7.4, engine="MolSysMT", in_place=False, skip_digestion=False
):
    """
    Removing hydrogens inconsistent with supported pH/reference inventories.

    This complements add_missing_hydrogens by removing rather than adding atoms.
    Standard labels use the existing fixed-pKa approximation. Explicit named Amber
    states constrain their side-chain inventory; unsupported references remain
    unassessed and unchanged. This does not predict an environmental pKa or select
    a stored chemical state.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of the supported forms.
    pH : float, default=7.4
        Finite dimensionless pH for the existing fixed-pKa reference comparison.
    engine : str, default='MolSysMT'
        Engine used to decide the protonation states. Only `'MolSysMT'` is supported.
    in_place : bool, default=False
        True publishes a prepared subset on the original native MolSys and returns
        None. False returns an independent native MolSys, including no-op results
        and supported file/complementary inputs.
    skip_digestion : bool, default=False
        If `True`, the input arguments are not digested.

    Returns
    -------
    molsysmt.MolSys or None
        Independent native output, or None after native in-place execution.

    Raises
    ------
    NotImplementedMethodError
        If an engine other than `'MolSysMT'` is requested.

    Notes
    -----
    The native reference query reads each group's stored naming convention and
    never substitutes a sequence parent. Explicit Amber-state side-chain inventories
    stay constrained by their label, even at a different pH. Named-state terminal
    completion, unsupported profile/name pairs and incompatible atom layouts are
    unassessed, so their hydrogens are not removed. Undeclared ambiguous names fail
    before candidate preparation. Stored source components are never rebuilt.
    Use a fixed-state workflow when the stored
    chemical assignments must determine the intended state independently of names.

    Only amino-acid residues are assessed. A residue with no entry in the template
    database has no expectation to compare against, so its hydrogens are never removed —
    silence about a residue means *not assessed*, not *correct*.

    For a preview, call assess_protonation and inspect its detached report and
    canonical bidirectional atom map. Its apply() method consumes the same
    source-bound decision once without repeating inference. This convenience
    function performs those two steps together. A complete candidate precedes
    publication; preparation failures leave the source unchanged. Native in-place
    no-ops retain domain identities; independent no-ops are real copies.
    The reference state supplies the rule's connectivity context. Removing atoms
    projects the shared atom axis in every stored state and every structure;
    other chemical states are not certified by the reference-state comparison.

    .. warning::

       The protonation states come from the same **fixed pKa thresholds** as
       `add_missing_hydrogens`, taken from free-amino-acid values rather than computed
       for each residue in its environment. Removing a hydrogen is a destructive act
       decided by an approximation: a deposited hydrogen may be experimental evidence
       that a residue titrates away from its textbook threshold. Where the assignment
       matters, check what this removes rather than assuming it.

    See Also
    --------
    :func:`molsysmt.build.add_missing_hydrogens`
        The complementary operation, which only adds.
    assess_protonation
        Prepare inspectable removal maps without changing the source.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['chicken villin HP35']['1vii.pdb'],
    ...                      to_form='molsysmt.MolSys')
    >>> result = msm.build.reconcile_protonation(molsys, pH=12.0)
    >>> (molsys.get(n_atoms=True), result.get(n_atoms=True))
    (596, 590)

    .. admonition:: User guide

       See :ref:`Tutorial_Protonation_Assessment` for preview and execution modes.

    .. versionadded:: 1.0.0
    """

    if in_place:
        from molsysmt.native._subset import validate_removal_target

        validate_removal_target(molecular_system, None)
    from .assess_protonation import assess_protonation

    assessment = assess_protonation(
        molecular_system, pH=pH, engine=engine, skip_digestion=True
    )
    return assessment.apply(molecular_system, in_place=in_place, skip_digestion=True)
