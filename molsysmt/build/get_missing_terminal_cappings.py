from molsysmt._private.argdigest import arg_digest

@arg_digest()
def get_missing_terminal_cappings(molecular_system, selection='all', syntax='MolSysMT', engine='MolSysMT'):
    """
    Identify terminal capping atoms that are missing from chain termini in a molecular system.

    This function detects atoms expected at the C-terminus of protein chains that are
    absent from the current structure. Currently the only terminal heavy atom checked is
    ``OXT`` (C-terminal oxygen). The result maps group (residue) indices to the list of
    missing terminal atoms.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.

    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Atom selection used to restrict the search to a subset of the system.

    syntax : str, default 'MolSysMT'
        Syntax used to interpret the ``selection`` string.

    engine : {'MolSysMT', 'PDBFixer'}, default 'MolSysMT'
        Backend used to detect missing terminal atoms.

        * ``'MolSysMT'``: native implementation.  For each chain, identifies
          the C-terminal amino-acid residue (last by group sequence number) and
          checks whether ``OXT`` is present.  Works with any supported form; no
          external dependency required.
        * ``'PDBFixer'``: delegates to ``pdbfixer.findMissingAtoms`` /
          ``missingTerminals``.

    Returns
    -------
    dict
        Dictionary mapping group (residue) indices (int) in the original molecular
        system to lists of missing terminal atom names (list of str). Only terminal
        groups with missing cappings are included.

    Raises
    ------
    NotImplementedError
        Raised if the requested ``engine`` is not supported.

    Notes
    -----
    When ``engine='MolSysMT'`` the C-terminal residue of each chain is found by
    sorting the chain's amino-acid groups by their group sequence number (``group_id``
    cast to ``int``) and taking the last one.  This correctly handles structures
    where group indices are not stored in chain-sequence order (e.g. multi-model
    assemblies).

    Non-amino-acid chains (water, ions, small molecules) are silently skipped.

    .. versionadded:: 1.0.0
    """

    output = {}

    if engine == 'MolSysMT':

        from molsysmt.basic import select, get
        from molsysmt.element.group.amino_acid import group_names as aa_names

        # All groups in the selection, keyed by chain
        group_indices = select(molecular_system, element='group', selection=selection, syntax=syntax)

        # Per-group: chain index, group_id, group_name
        chain_index_per_group = get(molecular_system, element='group', selection=group_indices,
                                    chain_index=True, skip_digestion=True)
        group_id_per_group = get(molecular_system, element='group', selection=group_indices,
                                 group_id=True, skip_digestion=True)
        group_name_per_group = get(molecular_system, element='group', selection=group_indices,
                                   group_name=True, skip_digestion=True)

        # Collect amino-acid groups per chain: {chain_idx: [(group_id_int, group_idx), ...]}
        chain_aa_groups: dict = {}
        for group_idx, chain_idx, group_id, group_name in zip(
            group_indices, chain_index_per_group, group_id_per_group, group_name_per_group
        ):
            if group_name not in aa_names:
                continue
            try:
                gid_int = int(group_id)
            except (ValueError, TypeError):
                gid_int = 0
            chain_aa_groups.setdefault(int(chain_idx), []).append((gid_int, int(group_idx)))

        # Also collect ALL groups per chain (sorted by group_id) to detect
        # capping groups that follow the last amino acid.
        chain_all_groups: dict = {}
        for group_idx, chain_idx, group_id in zip(
            group_indices, chain_index_per_group, group_id_per_group
        ):
            try:
                gid_int = int(group_id)
            except (ValueError, TypeError):
                gid_int = 0
            chain_all_groups.setdefault(int(chain_idx), []).append((gid_int, int(group_idx)))

        for chain_idx, aa_list in chain_aa_groups.items():
            # Sort by group sequence number; take the last (C-terminal) residue.
            aa_list.sort(key=lambda x: x[0])
            last_aa_gid, c_term_group_idx = aa_list[-1]

            # If the very last group in the chain (by group_id) is NOT an amino
            # acid (e.g. NME, ACE capping group), OXT is not expected.
            all_list = chain_all_groups[chain_idx]
            all_list.sort(key=lambda x: x[0])
            last_any_gid, _ = all_list[-1]
            if last_any_gid != last_aa_gid:
                continue  # chain is C-terminally capped

            atom_names = get(molecular_system, element='atom',
                             selection=list(
                                 get(molecular_system, element='group',
                                     selection=c_term_group_idx, atom_index=True,
                                     skip_digestion=True)[0]
                             ),
                             atom_name=True, skip_digestion=True)

            if 'OXT' not in atom_names:
                output[c_term_group_idx] = ['OXT']

    elif engine == "PDBFixer":

        from molsysmt.basic import convert, get_form, select

        group_indices_in_selection = select(molecular_system, element='group', selection=selection)

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer",
                                        selection=selection, syntax=syntax)

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()

        for group, atoms in temp_molecular_system.missingTerminals.items():
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index] = atoms

    else:

        raise NotImplementedError

    return output
