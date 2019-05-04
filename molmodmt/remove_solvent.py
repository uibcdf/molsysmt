
def remove_solvent (item, ions=False, include_selection=None, exclude_selection=None,
                   syntaxis='mdtraj'):

    atoms_list_to_be_removed = []
    atoms_list_water = []
    atoms_list_ions = []
    atoms_list_included = []
    atoms_list_excluded = []

    atoms_list_water = _select(item,'water')

    if ions:
        atoms_list_ions = _select(item,'resname '+)
