from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def get_missing_terminal_cappings(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer'):
    """
    Identify terminal capping atoms that are missing from chain termini in a molecular system.

    This function detects atoms expected at the N- or C-termini of protein chains
    that are absent from the current structure. The result maps group (residue)
    indices to the list of missing terminal atoms reported by the backend.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.

    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Atom selection used to restrict the search to a subset of the system.

    syntax : str, default 'MolSysMT'
        Syntax used to interpret the ``selection`` string.

    engine : {'PDBFixer'}, default 'PDBFixer'
        Backend used to detect missing terminal atoms. Only 'PDBFixer' is currently
        supported.

    Returns
    -------
    dict
        Dictionary mapping group (residue) indices (int) in the original molecular
        system to lists of missing terminal atom or capping descriptors as reported
        by the backend. Only terminal groups with missing cappings are included.

    Raises
    ------
    NotImplementedError
        Raised if the requested ``engine`` is not supported.

    Notes
    -----
    The function converts the (sub)system to a ``pdbfixer.PDBFixer`` object, calls
    ``findMissingResidues`` and ``findMissingAtoms`` to populate
    ``missingTerminals``, and maps the PDBFixer-internal residue indices back to
    the original group indices in the molecular system.

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
        missingAtoms = temp_molecular_system.missingTerminals

        for group, atoms in temp_molecular_system.missingTerminals.items():
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index]=atoms

    else:

        raise NotImplementedError

    return output

