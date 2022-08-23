from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_atoms_with_alternate_locations(molecular_system):

    from molsysmt.basic import get

    output_atoms = []

    alternate_location = get(molecular_system, element='atom', alternate_location=True)

    if not np.all(alternate_location==None):

        atom_indices = np.where(alternate_location!=None)[0]
        atom_name, group_id, chain_id = get(molecular_system, element='atom',
                                            selection=atom_indices, atom_name=True, group_id=True,
                                            chain_id=True)
        for ii, alt_loc in enumerate(alternate_location[atom_indices]):
            if alt_loc=='A':
                mask_atom_name = (atom_name == atom_name[ii])
                mask_group_id = (group_id == group_id[ii])
                mask_chain_id = (chain_id == chain_id[ii])
                mask = mask_atom_name*mask_group_id*mask_chain_id
                output_atoms.append(atom_indices[mask])

    return output_atoms

