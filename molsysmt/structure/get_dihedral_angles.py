import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest
from molsysmt.basic import get
from molsysmt import lib as msmlib
import gc

@digest()
def get_dihedral_angles(molecular_system, selection='all', dihedral_quartets=None,
                        structure_indices='all', syntax='MolSysMT', pbc=False, **kwargs):
    """
    To be written soon...
    """

    # phi, psi, omega, chi1, chi2, chi3, chi4, chi5

    angles_split=None

    if dihedral_quartets is None:

        from molsysmt.topology import get_dihedral_quartets

        dihedral_quartets = []
        angles_split=[]
        for key in kwargs.keys():
            if kwargs[key]:
                aux_dihedral_quartets = get_dihedral_quartets(molecular_system, selection=selection,
                                                     syntax=syntax, **{key:True})
                dihedral_quartets.append(aux_dihedral_quartets)
                angles_split.append(len(aux_dihedral_quartets))
        dihedral_quartets = np.concatenate(dihedral_quartets)

    atom_indices=[]
    n_quartets=dihedral_quartets.shape[0]
    aux_dihedral_quartets=np.zeros((n_quartets,4), dtype=np.int64)
    aux_dict={}
    mm=0
    for ii in range(n_quartets):
        for jj in range(4):
            kk = dihedral_quartets[ii,jj]
            if kk in aux_dict:
                aux_dihedral_quartets[ii,jj]=aux_dict[kk]
            else:
                aux_dict[kk]=mm
                atom_indices.append(kk)
                aux_dihedral_quartets[ii,jj]=mm
                mm+=1
    dihedral_quartets=aux_dihedral_quartets
    del(aux_dict, aux_dihedral_quartets)

    coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    coordinates, length_unit = puw.get_value_and_unit(coordinates)

    if pbc:

        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

        if box is not None:
            if box[0] is not None:
                box = puw.get_value(box, to_unit=length_unit)
                angles = msmlib.structure.get_mic_dihedral_angles(coordinates, box, dihedral_quartets)
                del(coordinates, box, dihedral_quartets)
            else:
                pbc = False
        else:
            pbc = False

    if not pbc:

        angles = msmlib.structure.get_dihedral_angles(coordinates, dihedral_quartets)
        del(coordinates, dihedral_quartets)


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

