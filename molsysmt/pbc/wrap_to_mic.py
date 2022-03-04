from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
from molsysmt.lib import box as libbox
import numpy as np
from molsysmt import puw

def wrap_to_mic(molecular_system, selection='all', structure_indices='all',
                center='[0,0,0] nanometers', center_of_selection=None, weights_for_center=None,
                recenter=True, keep_covalent_bonds=False,
                syntaxis='MolSysMT', engine='MolSysMT', in_place=False):

    engine = digest_engine(engine)
    structure_indices = digest_structure_indices(structure_indices)

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract, copy

        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)

        coordinates= get(molecular_system, target='atom', indices=atom_indices, coordinates=True)
        length_units = puw.get_unit(coordinates)
        n_structures = coordinates.shape[0]
        n_atoms = coordinates.shape[1]
        box, box_shape = get(molecular_system, target='system', structure_indices=structure_indices, box=True, box_shape=True)
        box = puw.convert(box, to_unit=length_units)

        orthogonal = 0
        if box_shape is None:
            raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
        elif box_shape == 'cubic':
            orthogonal =1

        if center_of_selection is not None:

            from molsysmt.structure import get_center
            center = get_center(molecular_system, selection=center_of_selection,
                                weights=weights_for_center, structure_indices=structure_indices,
                                syntaxis=syntaxis, engine='MolSysMT')

            center = puw.convert(center, to_unit=length_units)
            center = puw.get_value(center)

        else:

            center = puw.quantity(center)
            center = puw.convert(center, to_unit=length_units)
            center = puw.get_value(center)

            center_shape = np.shape(center)
            if len(center_shape)==1 and center_shape[-1]==3:
                center = np.tile(center,[n_structures,1,1])
            elif len(center_shape)==2 and center_shape[-1]==3 and center_shape[0]==n_structures:
                center = np.expand_dims(center, axis=1)
            elif len(center_shape)==2 and center_shape[-1]==3 and center_shape[0]==1:
                center = np.tile(center[0],[n_structures,1,1])
            elif len(center_shape)==3 and center_shape[-1]==3 and center_shape[0]==n_structures and center_shape[1]==1:
                center = np.array(center)
            else:
                raise ValueError('center needs the right shape')

        box = np.asfortranarray(puw.get_value(box), dtype='float64')
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        center = np.asfortranarray(center, dtype='float64')

        libbox.wrap_mic(coordinates, center, box, orthogonal, n_atoms, n_structures)

        if recenter:
            translation = np.tile(-center,(n_atoms,1))
            coordinates+=translation

        coordinates=np.ascontiguousarray(coordinates)*length_units

    else:

        raise NotImpementedEngineError()

    if in_place:

        set(molecular_system, target='atom', indices=atom_indices, structure_indices=structure_indices,
                syntaxis=syntaxis, coordinates=coordinates)

        pass

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, target='atom', indices=atom_indices, structure_indices=structure_indices,
            syntaxis=syntaxis, coordinates=coordinates)

        return tmp_molecular_system


