from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def get_center_of_mass(molecular_system, selection='all', groups_of_atoms=None,
        structure_indices='all', syntax='MolSysMT', engine='MolSysMT', parallel=False, check=True):

    from molsysmt.structure.get_center import get_center

    return get_center(molecular_system, selection=selection, groups_of_atoms=groups_of_atoms, weights='masses', structure_indices=structure_indices, syntax=syntax,
                      engine=engine, parallel=parallel, check=check)
