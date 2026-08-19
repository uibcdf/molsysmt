from molsysmt._private.argdigest import arg_digest


@arg_digest()
def reconcile_protonation(molecular_system, pH=7.4, engine='MolSysMT', in_place=False,
                          skip_digestion=False):
    """
    Removing the hydrogen atoms a molecular system carries that the pH does not call for.

    `molsysmt.build.add_missing_hydrogens` only adds. A hydrogen already present that
    the requested pH contradicts is left untouched, so a system that arrives protonated
    — an NMR structure, or one prepared earlier at a different pH — keeps a protonation
    state nobody asked for. This function is the other half of that comparison.

    It removes and never adds. Run it before `add_missing_hydrogens` to bring an
    incoming structure to the requested pH, then add what is missing.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of the supported forms.
    pH : float, default=7.4
        The pH the resulting protonation must correspond to.
    engine : str, default='MolSysMT'
        Engine used to decide the protonation states. Only `'MolSysMT'` is supported.
    in_place : bool, default=False
        If `True`, the input system is modified and `None` is returned.
    skip_digestion : bool, default=False
        If `True`, the input arguments are not digested.

    Returns
    -------
    molecular system
        A copy with the unwanted hydrogens removed, or `None` if `in_place=True`.

    Raises
    ------
    NotImplementedMethodError
        If an engine other than `'MolSysMT'` is requested.

    Notes
    -----
    Only amino-acid residues are assessed. A residue with no entry in the template
    database has no expectation to compare against, so its hydrogens are never removed —
    silence about a residue means *not assessed*, not *correct*.

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

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['chicken villin HP35']['1vii.pdb'],
    ...                      to_form='molsysmt.MolSys')   # doctest: +SKIP
    >>> molsys = msm.build.reconcile_protonation(molsys, pH=12.0)   # doctest: +SKIP

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.smonitor import NotImplementedMethodError

    if engine != 'MolSysMT':
        raise NotImplementedMethodError(
            caller='molsysmt.build.reconcile_protonation',
            message=f"engine='{engine}' is not implemented; only 'MolSysMT' is available.",
        )

    from molsysmt.basic import convert, get_form, remove
    from molsysmt.build._protonation import unexpected_hydrogens

    form_in = get_form(molecular_system)
    native_molsys = (molecular_system if form_in == 'molsysmt.MolSys'
                     else convert(molecular_system, to_form='molsysmt.MolSys',
                                  skip_digestion=True))

    unexpected = unexpected_hydrogens(native_molsys, pH=pH)

    if not unexpected:
        if in_place:
            return None
        return convert(molecular_system, to_form=form_in, skip_digestion=True)

    atom_indices = [entry[0] for entry in unexpected]

    output = remove(molecular_system, selection=atom_indices, in_place=in_place,
                    skip_digestion=True)

    if in_place:
        return None
    return output
