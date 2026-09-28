from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_missing_heavy_atoms(
    molecular_system, selection="all", syntax="MolSysMT", engine="MolSysMT"
):
    """
    Identify heavy (non-hydrogen) atoms that are missing from residues in a molecular system.

    This function compares the heavy atoms present in each residue against standard
    residue templates and returns a mapping of residue (group) indices to the names
    of atoms that are absent from the structure.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : object, default='MolSysMT'
        Argument engine.

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
    amino-acid topology database or an exact curated modified-residue template via
    :func:`~molsysmt.element.group.amino_acid.get_expected_heavy_atoms`.  The
    topology variant whose atom set is a superset of the present heavy atoms is
    selected; missing atoms are the set difference between expected and present.

    Only residues with an exact chemical template are assessed. MSE and SEP
    use their own component templates; other modified residues without an exact
    template remain unassessed rather than being treated as their nearest
    standard sequence equivalents. Water, ions, and ligands are also skipped.


    .. versionadded:: 1.0.0
    """

    output = {}

    if engine == "MolSysMT":
        from molsysmt.basic import get, select
        from molsysmt.element.group.amino_acid import (
            get_expected_heavy_atoms,
        )
        from molsysmt.element.group.amino_acid.get_expected_heavy_atoms import (
            _is_hydrogen,
        )

        # Terminal-only heavy atoms handled separately by get_missing_terminal_cappings
        _TERMINAL_HEAVY_ATOMS = {"OXT"}

        group_indices = select(
            molecular_system, element="group", selection=selection, syntax=syntax
        )
        group_name_list = get(
            molecular_system,
            element="group",
            selection=group_indices,
            group_name=True,
            skip_digestion=True,
        )
        atom_indices_per_group = get(
            molecular_system,
            element="group",
            selection=group_indices,
            atom_index=True,
            skip_digestion=True,
        )
        # Fetch all atom names in one call to avoid O(n_groups) digestion overhead
        all_atom_names = get(
            molecular_system,
            element="atom",
            selection="all",
            atom_name=True,
            skip_digestion=True,
        )

        for group_idx, group_name, atom_idx_list in zip(
            group_indices, group_name_list, atom_indices_per_group
        ):
            actual_atom_names = [all_atom_names[i] for i in atom_idx_list]

            expected_heavy = get_expected_heavy_atoms(group_name, actual_atom_names)
            if expected_heavy is None:
                continue

            actual_heavy = {a for a in actual_atom_names if not _is_hydrogen(a)}
            missing = (expected_heavy - actual_heavy) - _TERMINAL_HEAVY_ATOMS

            if missing:
                output[int(group_idx)] = sorted(missing)

    elif engine == "PDBFixer":
        from molsysmt.basic import convert, select

        group_indices_in_selection = select(
            molecular_system, element="group", selection=selection
        )

        temp_molecular_system = convert(
            molecular_system,
            to_form="pdbfixer.PDBFixer",
            selection=selection,
            syntax=syntax,
        )

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()

        for group, atoms in temp_molecular_system.missingAtoms.items():
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index] = []
            for atom in atoms:
                output[original_group_index].append(atom.name)

    else:
        raise NotImplementedError

    return output
