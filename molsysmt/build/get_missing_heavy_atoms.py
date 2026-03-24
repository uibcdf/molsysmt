from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def get_missing_heavy_atoms(molecular_system, selection='all', syntax='MolSysMT', engine='MolSysMT'):
    """
    Identify heavy (non-hydrogen) atoms that are missing from residues in a molecular system.

    This function compares the heavy atoms present in each residue against standard
    residue templates and returns a mapping of residue (group) indices to the names
    of atoms that are absent from the structure.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.

    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Atom selection used to restrict the search to a subset of groups.

    syntax : str, default 'MolSysMT'
        Syntax used to interpret the ``selection`` string.

    engine : {'MolSysMT', 'PDBFixer'}, default 'MolSysMT'
        Backend used to identify missing atoms.

        * ``'MolSysMT'``: native implementation using MolSysMT's amino-acid
          topology database.  Compares the heavy atoms present in each residue
          against the best-matching topology variant.  Works with any supported
          form; no external dependency required.
        * ``'PDBFixer'``: delegates to ``pdbfixer.findMissingAtoms``.

    Returns
    -------
    dict
        Dictionary mapping group (residue) indices (int) in the original molecular
        system to lists of missing atom names (list of str). Groups with no missing
        atoms are not included.

    Raises
    ------
    NotImplementedError
        Raised if the requested ``engine`` is not supported.

    Notes
    -----
    When ``engine='MolSysMT'`` the expected heavy atoms are obtained from the
    amino-acid topology database via
    :func:`~molsysmt.element.group.amino_acid.get_expected_heavy_atoms`.  The
    topology variant whose atom set is a superset of the present heavy atoms is
    selected; missing atoms are the set difference between expected and present.

    Only amino-acid residues (including recognized non-standard forms) are
    processed; water, ions, and ligands are silently skipped.

    .. versionadded:: 1.0.0
    """

    output = {}

    if engine == 'MolSysMT':

        from molsysmt.basic import select, get
        from molsysmt.element.group.amino_acid import (
            group_names as aa_names, get_expected_heavy_atoms, get_standard_name
        )
        from molsysmt.element.group.amino_acid.get_expected_heavy_atoms import _is_hydrogen

        # Terminal-only heavy atoms handled separately by get_missing_terminal_cappings
        _TERMINAL_HEAVY_ATOMS = {'OXT'}

        group_indices = select(molecular_system, element='group', selection=selection, syntax=syntax)
        group_name_list = get(molecular_system, element='group', selection=group_indices,
                              group_name=True)
        atom_indices_per_group = get(molecular_system, element='group', selection=group_indices,
                                     atom_index=True)

        for group_idx, group_name, atom_idx_list in zip(group_indices, group_name_list,
                                                        atom_indices_per_group):
            # Determine the canonical look-up name
            canonical = get_standard_name(group_name)
            lookup_name = canonical if canonical is not None else group_name
            if lookup_name not in aa_names:
                continue

            actual_atom_names = get(molecular_system, element='atom',
                                    selection=list(atom_idx_list), atom_name=True)

            expected_heavy = get_expected_heavy_atoms(lookup_name, actual_atom_names)
            if expected_heavy is None:
                continue

            actual_heavy = {a for a in actual_atom_names if not _is_hydrogen(a)}
            missing = (expected_heavy - actual_heavy) - _TERMINAL_HEAVY_ATOMS

            if missing:
                output[int(group_idx)] = sorted(missing)

    elif engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        group_indices_in_selection = select(molecular_system, element='group', selection=selection)

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer", selection=selection,
                                        syntax=syntax)

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()

        for group, atoms in temp_molecular_system.missingAtoms.items():
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index]=[]
            for atom in atoms:
                output[original_group_index].append(atom.name)

    else:

        raise NotImplementedError


    return output

