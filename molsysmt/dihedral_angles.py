from .utils.frame_indices import digest as _digest_frame_indices
from .utils.forms import digest as _digest_forms
import numpy as _np
from .lib import geometry as _libgeometry

def get_dihedral_angles(item, quartets=None, frame_indices='all', pbc=False):

    from molsysmt import get
    from molsysmt.utils import units as msm_units

    if type(quartets) in [list,tuple]:
        quartets = _np.array(quartets, dtype=int)
    elif type(quartets) is _np.ndarray:
        pass
    else:
        raise ValueError

    shape = quartets.shape

    if len(shape)==1:
        if shape[0]==4:
            quartets=quartets.reshape([1,4])
        else:
            raise ValueError
    elif len(shape)==2:
        if shape[1]!=4:
            raise ValueError
    else:
        raise ValueError

    coordinates, box, box_shape = get(item, target='system', frame_indices=frame_indices, coordinates=True, box=True, box_shape=True)

    orthogonal = 0
    if box_shape is None:
        orthogonal =1
        if pbc:
            raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
    elif box_shape == 'cubic':
        orthogonal =1

    n_angles = quartets.shape[0]
    n_frames = coordinates.shape[0]
    n_atoms = coordinates.shape[1]

    if box is None:
        box= _np.zeros([n_frames,3,3])*msm_units.length

    box = _np.asfortranarray(box._value, dtype='float64')
    coordinates = _np.asfortranarray(coordinates._value, dtype='float64')

    angles = _libgeometry.dihedral_angles(coordinates, box, orthogonal, int(pbc), quartets, n_angles, n_atoms, n_frames)
    angles = _np.ascontiguousarray(angles)*msm_units.angle

    return angles

def ramachandran_angles(item, selection='all', frame_indices='all', syntaxis='MolSysMT', pbc=False,
                        plot=False):

    from .covalent import covalent_chains

    phi_covalent_chain = covalent_chains(item, chain='phi', selection=selection, syntaxis=syntaxis)
    psi_covalent_chain = covalent_chains(item, chain='psi', selection=selection, syntaxis=syntaxis)

    n_chains = phi_covalent_chain.shape[0]

    angles = get_dihedral_angles(item, quartets=_np.vstack([phi_covalent_chain, psi_covalent_chain]),
                                 frame_indices=frame_indices, pbc=pbc)

    return phi_covalent_chain, psi_covalent_chain, angles[:,:n_chains], angles[:,n_chains:]

def set_dihedral_angles(item, quartets=None, angles=None, angles_shifts=None, blocks=None, frame_indices='all', pbc=False,
                        to_form=None, engine='MolSysMT'):

    from molsysmt import get, convert
    from molsysmt import set as _set
    from molsysmt.utils import units as msm_units

    form_in, form_out = _digest_forms(item, to_form)
    frame_indices = _digest_frame_indices(item, frame_indices)

    if type(quartets) in [list,tuple]:
        quartets = _np.array(quartets, dtype=int)
    elif type(quartets) is _np.ndarray:
        pass
    else:
        raise ValueError

    shape = quartets.shape

    if len(shape)==1:
        if shape[0]==4:
            quartets=quartets.reshape([1,4])
        else:
            raise ValueError
    elif len(shape)==2:
        if shape[1]!=4:
            raise ValueError
    else:
        raise ValueError

    n_atoms = get(item, target='system', n_atoms=True)
    n_quartets = quartets.shape[0]
    n_frames = frame_indices.shape[0]

    if angles_shifts is not None:

        if type(angles_shifts._value) in [float]:
            if (n_quartets==1 and n_frames==1):
                angles_shifts = _np.array([[angles_shifts._value]], dtype=float)*angles_shifts.unit
            else:
                raise ValueError("angles_shifts do not match the number of frames and quartets")
        elif type(angles_shifts._value) in [list,tuple]:
            angles_shifts = _np.array(angles_shifts._value, dtype=float)*angles_shifts.unit
        elif type(angles_shifts._value) is _np.ndarray:
            pass
        else:
            raise ValueError

        shape = angles_shifts.shape

        if len(shape)==1:
            angles_shifts = angles_shifts.reshape([n_frames, n_quartets])

        angles = get_dihedral_angles(item, quartets=quartets, frame_indices=frame_indices, pbc=pbc)
        angles = angles + angles_shifts

    if type(angles._value) in [float]:
        if (n_quartets==1 and n_frames==1):
            angles = _np.array([[angles._value]], dtype=float)*angles.unit
        else:
            raise ValueError("angles do not match the number of frames and quartets")
    elif type(angles._value) in [list,tuple]:
        angles = _array(angles._value, dtype=float)*angles.unit
    elif type(angles._value) is _np.ndarray:
        pass
    else:
        raise ValueError

    shape = angles.shape

    if len(shape)==1:
        angles = angles.reshape([n_frames, n_quartets])

    if engine=='MolSysMT':

        if blocks is None:

            from .covalent import covalent_blocks

            blocks = _np.zeros([n_quartets, n_atoms], dtype=int)

            for quartet_index in range(n_quartets):

                quartet = quartets[quartet_index]
                blocks[quartet_index,:] = covalent_blocks(item, remove_bonds=[quartet[1], quartet[2]], output_form='array')

        coordinates, box, box_shape = get(item, target='system', frame_indices=frame_indices, coordinates=True, box=True, box_shape=True)

        orthogonal = 0
        if box_shape is None:
            orthogonal =1
            if pbc:
                raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
        elif box_shape == 'cubic':
            orthogonal =1

        if box is None:
            box= _np.zeros([n_frames,3,3])*msm_units.length

        box = _np.asfortranarray(box._value, dtype='float64')

        length_units = coordinates.unit
        coordinates = _np.asfortranarray(coordinates._value, dtype='float64')

        _libgeometry.set_dihedral_angles(coordinates, box, orthogonal, int(pbc), quartets, angles, blocks,
                                         n_quartets, n_atoms, n_frames)

        coordinates=_np.ascontiguousarray(coordinates)*length_units

        tmp_item = convert(item, to_form=form_out)
        _set(tmp_item, target='system', coordinates=coordinates, frame_indices=frame_indices)
        del(coordinates, length_units)
        return tmp_item

    else:

        raise NotImplementedError

