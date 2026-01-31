def view(molecular_system=None, selection='all', structure_indices='all', syntax='MolSysMT',
         skip_digestion=False):

    from molsysviewer import new_view

    return new_view(
        molecular_system=molecular_system,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        skip_digestion=skip_digestion,
    )
