
def remove_solvent (item, ions=False, include_selection=None, exclude_selection=None,
                   syntaxis='mdtraj'):

    from .multitool import select as _select
    from .multitool import extract as _extract
    from .utils.types import water_residues as _water_residues
    from .utils.types import ion_residues as _ion_residues

    atoms_list_to_be_removed = []
    atoms_list_water = []
    atoms_list_ions = []
    atoms_list_included = []
    atoms_list_excluded = []

    atoms_list_water = _select(item, 'resname '+' '.join([str(ii) for ii in _water_residues]),
                               syntaxis='mdtraj')

    if ions:
        atoms_list_ions = _select(item, 'resname '+' '.join([str(ii) for ii in _ion_residues]),
                                  syntaxis='mdtraj')

    if include_selection is not None:
        atoms_list_included = _select(item, include_selection, syntaxis=syntaxis)

    if exclude_selection is not None:
        atoms_list_excluded = _select(item, exclude_selection, syntaxis=syntaxis)

    atoms_list_to_be_removed = list(set(atoms_list_water) | set(atoms_list_ions) | set(atoms_list_included))
    atoms_list_to_be_removed = list(set(atoms_list_to_be_removed) - set(atoms_list_excluded))

    atoms_list_all = _select(item, 'all', 'mdtraj')
    atoms_list_survive = list(set(atoms_list_all) - set(atoms_list_to_be_removed))

    return _extract(item, atoms_list_survive)
