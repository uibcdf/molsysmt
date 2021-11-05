
def get_center_of_mass(molecular_system, selection='all', groups_of_atoms=None, frame_indices='all', syntaxis='MolSysMT', engine='MolSysMT', parallel=False):

    from molsysmt.structure.get_center import get_center

    return get_center(molecular_system, selection=selection, groups_of_atoms=groups_of_atoms, weights='masses', frame_indices=frame_indices, syntaxis=syntaxis,
                      engine=engine, parallel=parallel)
