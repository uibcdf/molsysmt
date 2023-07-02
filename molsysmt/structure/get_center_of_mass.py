from molsysmt._private.digestion import digest

@digest()
def get_center_of_mass(molecular_system, selection='all', groups_of_atoms=None,
        structure_indices='all', syntax='MolSysMT', engine='MolSysMT'):
    """
    To be written soon...
    """

    raise NotImplementedError

    from molsysmt.structure.get_center import get_center

    return get_center(molecular_system, selection=selection, groups_of_atoms=groups_of_atoms, weights=None, structure_indices=structure_indices, syntax=syntax,
                      engine=engine)
