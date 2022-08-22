from molsysmt._private.digestion import digest
import numpy as np

@digest()
def remove_atoms_with_alternate_locations(molecular_system, mode='highest_occupancy'):

    from molsysmt.basic import get_atoms_with_alternate_locations, get

    atoms_with_alt_loc = get_atoms_with_alternate_locations(molecular_system)


    if mode=='highest_occupancy':

        for atoms_list in atoms_with_alt_loc:

            alt_loc, occup = get(molecular_system, element='atom', selection=atoms_list,
                    alternate_location=True, occupancy=True)



    from molsysmt.basic import get, select

    output_atoms = []

    alternate_location = get(molecular_system, element='atom', alternate_location=True)

    for A_index in np.where(alternate_location=='A')[0]:

        atom_name, group_id, chain_id = get(molecular_system, element='atom',
                selection=A_index, atom_name=True, group_id=True, chain_id=True)

        equal_atoms = select(molecular_system, element='atom', selection='atom_name==@atom_name and group_id==@group_id and chain_id==@chain_id')

        output_atoms.append(equal_atoms)

    return output_atoms

