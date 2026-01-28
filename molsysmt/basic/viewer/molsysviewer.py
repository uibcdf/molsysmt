def view(molecular_system=None, selection='all', structure_indices='all', syntax='MolSysMT',
         skip_digestion=False):

    from molsysmt import convert

    if molecular_system is None:
        from molsysviewer import MolSysView
        return MolSysView()

    return convert(
        molecular_system,
        to_form='molsysviewer.MolSysView',
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        skip_digestion=True,
    )
