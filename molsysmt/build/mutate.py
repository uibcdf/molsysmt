from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    NotImplementedMethodError,
)


@signal(tags=["build", "mutation"])
@arg_digest()
def mutate(
    molecular_system,
    mutations=None,
    keys="group_index",
    selection="all",
    syntax="MolSysMT",
    engine="MolSysMT",
    *,
    skip_digestion=False,
):
    """
    Applying amino-acid substitutions with explicit reconstruction limits.

    This function replaces specified residues with different amino acids, rebuilds
    supported missing heavy atoms, and re-adds hydrogens when present in the input.
    The native engine can return an incomplete target group with an explicit
    warning; inspect its remaining heavy-atom inventory. The mutated structure
    is returned in the same form as the input.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    mutations : object, default=None
        Target substitutions as a group-keyed dictionary or mutation strings
        such as ``"VAL-1-GLY"`` (source name, group ID and target name).
        Required unless an empty dictionary or list is supplied for a copy.
    keys : object, default='group_index'
        Dictionary key meaning: ``group_index``, ``group_id`` or ``group_name``.
        Group indices are positions; group IDs are literal string labels.
        Use ``keys='group_name'`` explicitly for name-keyed dictionaries.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection restricting every mutation specification. Selecting any
        atom enables its entire group. Integers are atom indices; a Boolean mask
        has one entry per source atom. Repeated atoms enable each group once.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : object, default='MolSysMT'
        Reconstruction engine: ``MolSysMT`` for bounded native placement or
        ``PDBFixer`` for that optional provider's reconstruction.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
        Keyword-only; safety-critical target checks still apply.

    Returns
    -------
    molecular system
        A new molecular system with target amino-acid names and supported heavy
        atoms rebuilt. Unsupported native gaps remain missing with a warning.
        Hydrogens are re-added if the original system contained them. Returned
        in the same form as the input; the source is unchanged.
        Empty or disjoint valid requests return an independent copy without
        invoking reconstruction.


    Raises
    ------
    ArgumentError
        If atom/group indices, mutation names or string specifications are
        invalid, a group ID is unknown, or target substitutions conflict.
    ArgumentChoiceError
        If a selected mutation string's source name differs from the actual
        group name.

    StructuralInconsistencyError
        If an ID identifies several selected groups, or the optional provider's
        chain/ID addressing cannot distinguish the requested group.

    NotImplementedMethodError
        Raised if the requested ``engine`` is not supported.


    Notes
    -----
    Selection is resolved once on the source atom axis. Every request is
    intersected with its enabled groups, including index-keyed requests.
    Unmatched source-name keys are ignored. Unknown group IDs and out-of-range
    group indices are errors, even when selection is empty. Source-name checks
    apply to selected string requests. Selected ambiguous IDs require a narrower
    selection. Identical repeated substitutions are deduplicated; conflicting
    targets for one selected group are rejected before engine edits.

    Target amino-acid names are converted to uppercase. Native mutation removes
    non-backbone atoms from each target and delegates reconstruction to
    ``add_missing_heavy_atoms(engine='MolSysMT')`` on target groups. Its preflight
    rejects multiple missing side-chain atoms, invalid anchors and conflicting
    local geometry with ``UnassessedResidueWarning``. For example, a target TRP
    can retain only its observed backbone. Inspect ``get_missing_heavy_atoms``
    on the result: the target name and added H do not certify complete chemistry,
    a validated rotamer, resolved clashes or an energy minimum.

    The explicit ``PDBFixer`` engine uses ``applyMutations``,
    ``findMissingResidues``, ``findMissingAtoms`` and ``addMissingAtoms``.
    It can reconstruct inventories outside native coverage; matching atom counts
    does not independently validate those coordinates. No automatic engine
    fallback is performed.
    PDBFixer requires non-negative integer target IDs and unique integer IDs
    among groups sharing an addressed chain ID; ambiguous addresses are refused.
    Its PDB-text conversion rounds retained coordinates to 0.001 angstrom.
    PDBFixer heavy-atom repair and hydrogen completion in either engine retain
    their whole-system scope: selection restricts substitutions, not every
    possible repair. Native heavy-atom repair is restricted to target groups.

    See Also
    --------
    molsysmt.build.get_missing_heavy_atoms
        Inspecting unresolved heavy-atom inventories after mutation.
    molsysmt.build.add_missing_heavy_atoms
        Reconstructing gaps within the selected engine's geometric coverage.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.build.build_peptide('AlaValPro')
    >>> new_molsys = msm.build.mutate(molsys, mutations={1: 'GLY'})
    >>> msm.get(new_molsys, element='group', group_name=True)
    ['ALA', 'GLY', 'PRO']
    >>> msm.build.get_missing_heavy_atoms(new_molsys)
    {}
    >>> atom_indices = msm.select(molsys, 'group_index==1')
    >>> new_molsys = msm.build.mutate(molsys, {'VAL': 'GLY'},
    ...     keys='group_name', selection=atom_indices[:1])
    >>> msm.get(new_molsys, element='group', group_name=True)
    ['ALA', 'GLY', 'PRO']

    .. admonition:: User guide

       See :ref:`Tutorial_Mutate` for mutation specifications and reconstruction limits.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import copy
    from molsysmt.build._mutation_targets import resolve_mutation_targets

    if engine not in ("MolSysMT", "PDBFixer"):
        raise NotImplementedMethodError
    targets = resolve_mutation_targets(
        molecular_system, mutations, keys, selection, syntax
    )
    if not targets:
        return copy(molecular_system)
    group_indices, to_group_names = map(list, zip(*targets))

    if engine == "PDBFixer":
        from molsysmt.basic import contains, convert, get_form
        from molsysmt.build._mutation_targets import pdbfixer_mutation_arguments

        form_in = get_form(molecular_system)
        had_h = contains(molecular_system, selection='atom_type=="H"')
        tmp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")

        arguments = pdbfixer_mutation_arguments(tmp_molecular_system, targets)
        for mutation_string, in_chain_id in arguments:
            tmp_molecular_system.applyMutations([mutation_string], in_chain_id)

        tmp_molecular_system.findMissingResidues()
        tmp_molecular_system.findMissingAtoms()
        tmp_molecular_system.addMissingAtoms()

        if had_h:
            tmp_molecular_system.addMissingHydrogens(7.4)

        tmp_molecular_system = convert(tmp_molecular_system, to_form=form_in)

        return tmp_molecular_system

    elif engine == "MolSysMT":
        from molsysmt.basic import contains, convert, get_form
        from molsysmt.basic import remove as msm_remove
        from molsysmt.build.add_missing_heavy_atoms import add_missing_heavy_atoms
        from molsysmt.build.add_missing_hydrogens import add_missing_hydrogens

        # Backbone heavy atoms that are kept across any amino-acid mutation.
        # OXT is retained when present (C-terminal residues).
        _BACKBONE_HEAVY = frozenset({"N", "CA", "C", "O", "OXT"})

        # ── convert to native form ───────────────────────────────────────────
        form_in = get_form(molecular_system)
        had_h = contains(molecular_system, selection='atom_type=="H"')
        tmp = convert(molecular_system, to_form="molsysmt.MolSys", skip_digestion=True)

        # ── 1. Rename groups ─────────────────────────────────────────────────
        for group_index, new_name in zip(group_indices, to_group_names):
            tmp.topology.groups.at[group_index, "group_name"] = new_name
            tmp.topology.groups.at[group_index, "group_type"] = "amino acid"
        tmp.topology._groups_dirty = True

        # ── 2. Strip non-backbone atoms from every mutated group ─────────────
        atoms_to_remove = []
        for group_index in group_indices:
            atoms_in_group = tmp.topology.atoms[
                tmp.topology.atoms["group_index"] == group_index
            ]
            non_backbone = atoms_in_group.index[
                ~atoms_in_group["atom_name"].isin(_BACKBONE_HEAVY)
            ].tolist()
            atoms_to_remove.extend(non_backbone)

        if atoms_to_remove:
            tmp = msm_remove(tmp, selection=atoms_to_remove, skip_digestion=True)

        # ── 3. Rebuild sidechain heavy atoms (Kabsch alignment on backbone) ──
        tmp = add_missing_heavy_atoms(tmp, selection=group_indices, engine="MolSysMT")

        # ── 4. Re-add hydrogens if original system had them ──────────────────
        if had_h:
            tmp = add_missing_hydrogens(tmp, engine="MolSysMT")

        return convert(tmp, to_form=form_in, skip_digestion=True)

    else:
        raise NotImplementedMethodError
