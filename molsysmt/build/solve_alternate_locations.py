from molsysmt._private.digestion import digest
import numpy as np

@digest()
def solve_alternate_locations(molecular_system, keep='A'):

    from molsysmt.basic import get, remove
    from molsysmt.build import get_atoms_with_alternate_locations

    atoms_to_be_removed = []

    if keep=='A':

        alt_loc = get(molecular_system, element='atom', alternate_location=True)

        if 'A' in alt_loc:

            mask_not_None = (alt_loc!=None)
            mask_not_A  = (alt_loc!='A')
            mask = mask_not_None*mask_not_A
            atoms_to_be_removed = np.argwhere(mask)[:,0]

    if len(atoms_to_be_removed)>1:
        return remove(molecular_system, selection=atoms_to_be_removed)
    else:
        return molecular_system

