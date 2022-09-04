from molsysmt._private.digestion import digest
import numpy as np
from scipy.spatial.transform import Rotation as R
from molsysmt import pyunitwizard as puw

@digest()
def rotate(molecular_system, rotation=None, selection='all', structure_indices='all',
        syntax='MolSysMT', in_place=False):

    from molsysmt.basic import get, set, select, copy

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    coordinates = get(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    if isinstance(rotation, np.ndarray):

        rotator = R.from_matrix(rotation)

    unit = puw.get_unit(coordinates)
    value = puw.get_value(coordinates)
    del(coordinates)

    new_coordinates = []
    for aux in value[:]:
        new_coordinates.append(rotator.apply(aux))
    new_coordinates = puw.quantity(np.array(new_coordinates), unit)

    if in_place:
        return set(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                   coordinates=new_coordinates)
    else:
        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
            coordinates=new_coordinates)
        return tmp_molecular_system

