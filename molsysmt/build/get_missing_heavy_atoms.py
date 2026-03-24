from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def get_missing_heavy_atoms(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer'):
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

    engine : {'PDBFixer'}, default 'PDBFixer'
        Backend used to identify missing atoms. Only 'PDBFixer' is currently
        supported.

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
    The function converts the (sub)system to a ``pdbfixer.PDBFixer`` object,
    calls ``findMissingResidues`` followed by ``findMissingAtoms``, and maps
    the PDBFixer-internal residue indices back to the original group indices in
    the molecular system.

    .. versionadded:: 1.0.0
    """

    output = {}

    if engine=="PDBFixer":

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

