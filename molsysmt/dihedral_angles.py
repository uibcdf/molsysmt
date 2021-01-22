from .tools.frame_indices import digest as _digest_frame_indices
from .tools.forms import digest as _digest_forms
import numpy as _np
from .lib import geometry as _libgeometry

def get_dihedral_angles(item, dihedral_angle=None, selection='all', quartets=None,
                        frame_indices='all', syntaxis='MolSysMT', pbc=False):

    from molsysmt import get
    from molsysmt.tools import units as msm_units

    if quartets is None:

        from molsysmt import covalent_dihedral_quartets

        quartets = covalent_dihedral_quartets(item, dihedral_angle=dihedral_angle,
                                              selection=selection, syntaxis=syntaxis)

    elif type(quartets) in [list,tuple]:
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


    coordinates = get(item, target='system', frame_indices=frame_indices, coordinates=True)

    n_angles = quartets.shape[0]
    n_frames = coordinates.shape[0]
    n_atoms = coordinates.shape[1]

    if pbc:

        box, box_shape = get(item, target='system', frame_indices=frame_indices, coordinates=True, box=True, box_shape=True)
        if box_shape is None:
            raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
        orthogonal = 0

        if box_shape is None:
            orthogonal =1
        elif box_shape == 'cubic':
            orthogonal =1

    else:

        orthogonal = 1
        box= _np.zeros([n_frames,3,3])*msm_units.length

    box = _np.asfortranarray(box._value, dtype='float64')
    coordinates = _np.asfortranarray(coordinates._value, dtype='float64')

    angles = _libgeometry.dihedral_angles(coordinates, box, orthogonal, int(pbc), quartets, n_angles, n_atoms, n_frames)
    angles = _np.ascontiguousarray(angles)*msm_units.angle

    return angles

def ramachandran_angles(item, selection='all', frame_indices='all', syntaxis='MolSysMT', pbc=False,
                        plot=False):

    from .covalent import covalent_dihedral_quartets
    from .tools.multiple_items import topology_and_trajectory_from_item

    topology_item, trajectory_item = topology_and_trajectory_from_item(item)

    phi_covalent_chain = covalent_dihedral_quartets(topology_item, dihedral_angle='phi', selection=selection, syntaxis=syntaxis)
    psi_covalent_chain = covalent_dihedral_quartets(topology_item, dihedral_angle='psi', selection=selection, syntaxis=syntaxis)

    n_chains = phi_covalent_chain.shape[0]

    angles = get_dihedral_angles(trajectory_item, quartets=_np.vstack([phi_covalent_chain, psi_covalent_chain]),
                                 frame_indices=frame_indices, pbc=pbc)

    return phi_covalent_chain, psi_covalent_chain, angles[:,:n_chains], angles[:,n_chains:]

def shift_dihedral_angles(item, quartets=None, angles_shifts=None, blocks=None,
                          frame_indices='all', pbc=False, in_place=True, engine='MolSysMT'):

    n_quartets = quartets.shape[0]
    n_frames = frame_indices.shape[0]

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

    return set_dihedral_angles(item, quartets=quartets, angles=angles, blocks=None,
                               frame_indices=frame_indices, pbc=pbc, in_place=inplace, engine=engine)

def set_dihedral_angles(item, quartets=None, angles=None, angles_shifts=None, blocks=None, frame_indices='all', pbc=False,
                        in_place=True, engine='MolSysMT'):

    from molsysmt import get, convert
    from molsysmt import set as _set
    from molsysmt.tools import units as msm_units

    form_in, _ = _digest_forms(item)
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

            blocks = []

            for quartet in quartets:

                tmp_blocks = covalent_blocks(item, remove_bonds=[quartet[1], quartet[2]])
                blocks.append(tmp_blocks)


        coordinates = get(item, target='system', frame_indices=frame_indices, coordinates=True)

        if pbc:

            box, box_shape = get(item, target='system', frame_indices=frame_indices, coordinates=True, box=True, box_shape=True)
            if box_shape is None:
                raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
            orthogonal = 0

            if box_shape is None:
                orthogonal =1
            elif box_shape == 'cubic':
                orthogonal =1

        else:

            orthogonal = 1
            box= _np.zeros([n_frames,3,3])*msm_units.length

        length_units = coordinates.unit
        box = _np.asfortranarray(box._value, dtype='float64')
        coordinates = _np.asfortranarray(coordinates._value, dtype='float64')

        aux_blocks = []
        aux_atoms_per_block = []

        for block in blocks:

            aux_atoms_per_block.append(len(block[1]))
            aux_blocks.append(list(block[1]))

        aux_blocks = _np.ravel(aux_blocks)
        aux_atoms_per_block = _np.array(aux_atoms_per_block, dtype=int)

        _libgeometry.set_dihedral_angles(coordinates, box, orthogonal, int(pbc), quartets, angles,
                                         aux_blocks, aux_atoms_per_block, n_quartets, n_atoms, n_frames, aux_blocks.shape[0])

        coordinates=_np.ascontiguousarray(coordinates)*length_units

        if in_place:
            return _set(item, target='system', coordinates=coordinates, frame_indices=frame_indices)
        else:
            from molsysmt import copy
            tmp_item = copy(item)
            _set(tmp_item, target='system', coordinates=coordinates, frame_indices=frame_indices)
            return tmp_item

    else:

        raise NotImplementedError

