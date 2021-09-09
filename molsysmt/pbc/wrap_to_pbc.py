from molsysmt._private_tools.engines import digest_engine
from molsysmt._private_tools.frame_indices import digest_frame_indices
from molsysmt._private_tools.forms import digest_form
from molsysmt._private_tools.box import digest_box_angles, digest_box_lengths
from molsysmt.lib import box as libbox
import numpy as np
from molsysmt import puw

def wrap_to_pbc(molecular_system, selection='all', frame_indices='all',
                center='[0,0,0] nanometers', center_of_selection=None, weights_for_center=None,
                recenter=True, keep_covalent_bonds=False,
                syntaxis='MolSysMT', engine='MolSysMT', in_place=False):

    engine = digest_engine(engine)
    frame_indices = digest_frame_indices(frame_indices)

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract, copy

        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)

        coordinates= get(molecular_system, target='atom', indices=atom_indices, coordinates=True)
        length_units = puw.get_unit(coordinates)
        n_frames = coordinates.shape[0]
        n_atoms = coordinates.shape[1]
        box, box_shape = get(molecular_system, target='system', frame_indices=frame_indices, box=True, box_shape=True)
        box = puw.convert(box, to_unit=length_units)

        orthogonal = 0
        if box_shape is None:
            raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
        elif box_shape == 'cubic':
            orthogonal =1

        if center_of_selection is not None:

            from molsysmt.structure import get_center
            center = get_center(molecular_system, selection=center_of_selection,
                                weights=weights_for_center, frame_indices=frame_indices,
                                syntaxis=syntaxis, engine='MolSysMT')

            center = puw.convert(center, to_unit=length_units)
            center = puw.get_value(center)

        else:

            center = puw.quantity(center)
            center = puw.convert(center, to_unit=length_units)
            center = puw.get_value(center)

            center_shape = np.shape(center)
            if len(center_shape)==1 and center_shape[-1]==3:
                center = np.tile(center,[n_frames,1,1])
            elif len(center_shape)==2 and center_shape[-1]==3 and center_shape[0]==n_frames:
                center = np.expand_dims(center, axis=1)
            elif len(center_shape)==2 and center_shape[-1]==3 and center_shape[0]==1:
                center = np.tile(center[0],[n_frames,1,1])
            elif len(center_shape)==3 and center_shape[-1]==3 and center_shape[0]==n_frames and center_shape[1]==1:
                center = np.array(center)
            else:
                raise ValueError('center needs the right shape')

        box = np.asfortranarray(puw.get_value(box), dtype='float64')
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        center = np.asfortranarray(center, dtype='float64')

        libbox.wrap_pbc(coordinates, center, box, orthogonal, n_atoms, n_frames)

        if recenter:
            translation = np.tile(-center,(n_atoms,1))
            coordinates+=translation

        coordinates=np.ascontiguousarray(coordinates)*length_units

    else:

        raise NotImpementedEngineError()

    if in_place:

        set(molecular_system, target='atom', indices=atom_indices, frame_indices=frame_indices,
                syntaxis=syntaxis, coordinates=coordinates)

        pass

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, target='atom', indices=atom_indices, frame_indices=frame_indices,
            syntaxis=syntaxis, coordinates=coordinates)

        return tmp_molecular_system

