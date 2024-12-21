import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest
from molsysmt import lib as msmlib
import gc

@digest()
def get_angles(molecular_system, triplets, structure_indices='all', pbc=False, skip_digestion=False):

    from molsysmt.basic import get

    atom_indices=[]
    n_triplets=triplets.shape[0]
    aux_triplets=np.zeros((n_triplets,3), dtype=np.int64)
    aux_dict={}
    mm=0
    for ii in range(n_triplets):
        for jj in range(3):
            kk = triplets[ii,jj]
            if kk in aux_dict:
                aux_triplets[ii,jj]=aux_dict[kk]
            else:
                aux_dict[kk]=mm
                atom_indices.append(kk)
                aux_triplets[ii,jj]=mm
                mm+=1
    triplets=aux_triplets
    del(aux_dict, aux_triplets)

    coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    coordinates, length_unit = puw.get_value_and_unit(coordinates)

    if pbc:

        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

        if box is not None:
            if box[0] is not None:
                box = puw.get_value(box, to_unit=length_unit)
                angles = msmlib.structure.get_mic_angles(coordinates, box, triplets)
                del(coordinates, box, triplets)
            else:
                pbc = False
        else:
            pbc = False

    if not pbc:

        angles = msmlib.structure.get_angles(coordinates, triplets)
        del(coordinates, triplets)


    angles = puw.quantity(angles, 'radians')
    angles = puw.standardize(angles)

    gc.collect()

    return angles

