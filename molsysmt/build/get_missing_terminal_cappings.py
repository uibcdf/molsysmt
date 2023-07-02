from molsysmt._private.digestion import digest

@digest()
def get_missing_terminal_cappings(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer'):
    """
    To be written soon...
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

