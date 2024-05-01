import numpy as np

_sorted=sorted

def get_bonded_atom_pairs(group_name, atom_names, atom_indices=None, sorted=True):

    n_atoms=len(atom_names)

    if n_atoms==1:

        return []

    elif n_atoms==2:

        return [atom_indices]
    
    else:

        raise NotImplementedError

