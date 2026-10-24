"""Applying a declared atom order through the owning native domains."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "basic"])
@arg_digest()
def permute_atoms(
    molecular_system, atom_indices, return_report=False, skip_digestion=False
):
    """Permuting a complete atom axis while preserving molecular correspondence.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form convertible to a native MolSys without implicit loss.
        Ready native MolSys inputs use their stored domains directly.
    atom_indices : list, tuple or numpy.ndarray
        Complete integer bijection in new-to-old order: atom_indices[new] is the
        original atom index. All atoms must occur exactly once. IDs are labels.
    return_report : bool, default=False
        Return a dictionary with molecular_system and a detached atom_map@1
        report when True; otherwise return the native molecular system alone.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys or dict
        Independent native domains on the requested atom axis. Other index axes,
        original scientific values and structure/state associations are retained.
        The optional report supplies both atom-map directions and original labels.

    Raises
    ------
    ArgumentError
        If the order is not a complete unit-free integer bijection.
    StructuralInconsistencyError
        If a present domain is inconsistent or outside the supported native profile.
    MemoryBudgetExceededError
        If the additional resident numeric output exceeds the configured budget.

    Notes
    -----
    This experimental operation applies a known permutation; it performs no
    chemical matching, inference or new parameter calculation. Extract remains
    a selection operation. Bond and stereo references, all chemical-state atom
    tables, structural series, mechanics and named interactions are remapped.
    Historical preparation records keep their original axes. Charge/type binding
    owners retain original producer credit and declare the derived transform.

    Protected coordinates use bounded ChunkedExecutor delivery. Full output
    remains resident; metadata/object overhead and the caller's source are outside
    the numeric-output estimate. Conversion of foreign forms has its own cost
    and information-loss contract. Unsupported extensions reject explicitly.

    See Also
    --------
    extract
        Extracting subsets of atoms and structures.
    compose_atom_maps
        Composing declared correspondence stages.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'])
    >>> result = permute_atoms(molsys, list(range(23, -1, -1)), return_report=True)
    >>> result['report']['output_to_source_atom_indices'][:3].tolist()
    [23, 22, 21]

    .. admonition:: User guide

       See :ref:`Tutorial_Permute_Atoms` and :ref:`Cookbook_Permuting_Export_Order`.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native import MolSys
    from molsysmt.native._atom_permutation import permute

    if not isinstance(molecular_system, MolSys):
        from molsysmt.basic import convert

        molecular_system = convert(molecular_system, to_form="molsysmt.MolSys")
    result, report = permute(
        molecular_system, atom_indices, return_report=return_report
    )
    return {"molecular_system": result, "report": report} if return_report else result
