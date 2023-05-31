import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest
from molsysmt.basic import get
from molsysmt import lib as msmlib
import gc

@digest()
def get_dihedral_angles(molecular_system, selection='all', quartets=None,
                        structure_indices='all', syntax='MolSysMT', pbc=False, **kwargs):

    # phi, psi, omega, chi1, chi2, chi3, chi4, chi5

    angles_split=None

    if quartets is None:

        from molsysmt.topology import get_dihedral_quartets

        quartets = []
        angles_split=[]
        for key in kwargs.keys():
            if kwargs[key]:
                aux_quartets = get_dihedral_quartets(molecular_system, selection=selection,
                                                     syntax=syntax, **{key:True})
                quartets.append(aux_quartets)
                angles_split.append(aux_quartets.shape[0])
        quartets = np.concatenate(quartets)

    atom_indices=[]
    n_quartets=quartets.shape[0]
    aux_quartets=np.zeros((n_quartets,4), dtype=np.int64)
    aux_dict={}
    mm=0
    for ii in range(n_quartets):
        for jj in range(4):
            kk = quartets[ii,jj]
            if kk in aux_dict:
                aux_quartets[ii,jj]=aux_dict[kk]
            else:
                aux_dict[kk]=mm
                atom_indices.append(kk)
                aux_quartets[ii,jj]=mm
                mm+=1
    quartets=aux_quartets
    del(aux_dict, aux_quartets)

    coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    coordinates, length_unit = puw.get_value_and_unit(coordinates)

    if pbc:

        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

        if box is not None:
            if box[0] is not None:
                box = puw.get_value(box, to_unit=length_unit)
                angles = msmlib.structure.get_mic_dihedral_angles(coordinates, box, quartets)
                del(coordinates, box, quartets)
            else:
                pbc = False
        else:
            pbc = False

    if not pbc:

        angles = msmlib.structure.get_dihedral_angles(coordinates, quartets)
        del(coordinates, quartets)


    angles = puw.quantity(angles, 'radians')
    angles = puw.standardize(angles)

    if angles_split is None:
        output=angles
    elif len(angles_split)==1:
        output=angles
    else:
        output = []
        ii=0
        for jj in angles_split:
            output.append(angles[:,ii:ii+jj])
            ii+=jj

    del(angles)
    gc.collect()

    return output

