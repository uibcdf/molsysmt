import numpy as np

def get_bonded_atom_pairs(group_name, atom_names, atom_indices=None, sorted=True):

    from . import group_names, get_group_db

    if group_name not in group_names:
        return []

    if atom_indices is None:
        atom_indices = np.arange(len(atom_names), dtype=int).tolist()

    db = get_group_db(group_name)

    is_in = -1
    for ii,jj in enumerate(db['topology']):
        if np.all(np.isin(atom_names, jj['atoms'])):
            is_in=ii
            break

    bonds = []
    if is_in!=-1:

        for ii,jj in db['topology'][is_in]['bonds']:
            if ii in atom_names:
                if jj in atom_names:
                    iii = atom_indices[atom_names.index(ii)]
                    jjj = atom_indices[atom_names.index(jj)]
                    if iii<jjj:
                        bonds.append([iii,jjj])
                    else:
                        bonds.append([jjj,iii])

    if sorted:
        from molsysmt._private.lists import sorted_list_of_pairs
        bonds = sorted_list_of_pairs(bonds)

    return bonds
