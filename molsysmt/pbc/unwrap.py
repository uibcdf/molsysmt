from molsysmt._private_tools.engines import digest_engine
from molsysmt._private_tools.frame_indices import digest_frame_indices
from molsysmt._private_tools.forms import digest_form
from molsysmt._private_tools.box import digest_box_angles, digest_box_lengths
from molsysmt.lib import box as libbox
import numpy as np
from molsysmt import puw

def unwrap(molecular_system, selection='all', frame_indices='all',
        syntaxis='MolSysMT', engine='MolSysMT', in_place=False):

    engine = digest_engine(engine)
    frame_indices = digest_frame_indices(frame_indices)

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract

        coordinates= get(molecular_system, target='atom', selection=selection, coordinates=True)
        n_frames = coordinates.shape[0]
        n_atoms = coordinates.shape[1]
        box, box_shape = get(molecular_system, target='system', frame_indices=frame_indices, box=True, box_shape=True)

        orthogonal = 0
        if box_shape is None:
            raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
        elif box_shape == 'cubic':
            orthogonal =1

        length_units = puw.get_unit(coordinates)
        box = puw.convert(box, to_unit=length_units)

        box = np.asfortranarray(puw.get_value(box), dtype='float64')
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')

        libbox.unwrap(coordinates, box, orthogonal, n_atoms, n_frames)

        coordinates=np.ascontiguousarray(coordinates)*length_units

    else:

        raise NotImpementedEngineError()

    if in_place:

        set(molecular_system, target='atom', selection=selection, frame_indices=frame_indices,
                syntaxis=syntaxis, coordinates=coordinates)

        pass

    else:

        tmp_molecular_system = extract(molecular_system, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)
        set(tmp_molecular_system, target='atom', selection='all', frame_indices='all', syntaxis='MolSysMT', coordinates=coordinates)

        return tmp_molecular_system

