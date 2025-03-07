from molsysmt._private.digestion import digest
import numpy as np


_sorted=sorted

@digest()
def get_bonded_atom_pairs(group_name, atom_names, atom_indices=None, sorted=True, skip_digestion=False):

    n_atoms=len(atom_names)

    if n_atoms==1:

        return []

    else:

        from molsysmt.element.group.ion import group_names, get_group_db

        if group_name not in group_names:
            raise ValueError
    
        if atom_indices is None:
            atom_indices = np.arange(len(atom_names), dtype=int).tolist()

        aux_group_names = [group_name]

        for aux_group_name in aux_group_names:

            db = get_group_db(aux_group_name)
            
            is_in = -1
            for ii,jj in enumerate(db['atom_name']):
                if np.all(np.isin(atom_names, jj)):
                    is_in=ii
                    break

            if is_in!=-1:

                bonds = []
                for i,j in db['bonds']:
                    ii = db['atom_name'][is_in][i]
                    jj = db['atom_name'][is_in][j]
                    if ii in atom_names:
                        if jj in atom_names:
                            iii = atom_indices[atom_names.index(ii)]
                            jjj = atom_indices[atom_names.index(jj)]
                            if iii<jjj:
                                bonds.append([iii,jjj])
                            else:
                                bonds.append([jjj,iii])
                if sorted:
                    return _sorted(bonds)
                else:
                    return bonds

