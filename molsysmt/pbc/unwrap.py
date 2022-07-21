from molsysmt._private.exceptions.not_implemented import NotImplementedEngineError
from molsysmt._private.digestion import *
from molsysmt import puw
from molsysmt.lib import box as libbox
import numpy as np

@digest
def unwrap(molecular_system, selection='all', structure_indices='all',
        syntax='MolSysMT', engine='MolSysMT', in_place=False):

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract

        coordinates= get(molecular_system, element='atom', selection=selection, coordinates=True)
        n_structures = coordinates.shape[0]
        n_atoms = coordinates.shape[1]
        box, box_shape = get(molecular_system, element='system', structure_indices=structure_indices, box=True,
                             box_shape=True)

        orthogonal = 0
        if box_shape is None:
            raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
        elif box_shape == 'cubic':
            orthogonal =1

        length_units = puw.get_unit(coordinates)
        box = puw.convert(box, to_unit=length_units)

        box = np.asfortranarray(puw.get_value(box), dtype='float64')
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')

        libbox.unwrap(coordinates, box, orthogonal, n_atoms, n_structures)

        coordinates=np.ascontiguousarray(coordinates)*length_units

    else:

        raise NotImplementedEngineError()

    if in_place:

        set(molecular_system, element='atom', selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        pass

    else:

        tmp_molecular_system = extract(molecular_system, selection=selection, structure_indices=structure_indices,
                                       syntax=syntax)
        set(tmp_molecular_system, element='atom', selection='all', structure_indices='all', syntax='MolSysMT',
            coordinates=coordinates)

        return tmp_molecular_system

