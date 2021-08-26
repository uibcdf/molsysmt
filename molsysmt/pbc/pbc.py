from molsysmt._private_tools.engines import digest_engine
from molsysmt._private_tools.frame_indices import digest_frame_indices
from molsysmt._private_tools.forms import digest_form
from molsysmt._private_tools.box import digest_box_angles, digest_box_lengths
from molsysmt.lib import box as libbox
import numpy as np
from molsysmt import puw

def box_shape_from_box_angles(angles):

    shape = None

    if angles is not None:

        alpha = angles[:,0].mean()
        beta = angles[:,1].mean()
        gamma = angles[:,2].mean()

        alpha = np.round(alpha, 2)
        beta = np.round(beta, 2)
        gamma = np.round(gamma, 2)

        if alpha==90.00 and beta==90.00 and gamma==90.00:
            shape = 'cubic'
        else:
            shape = 'triclinic'

    return shape

def box_shape_from_box_vectors(box):

    if box is None:
        return None
    else:
        tmp_box = np.asfortranarray(puw.get_value(box), dtype='float64')
        n_frames = tmp_box.shape[0]
        angles = libbox.angles_box(tmp_box, n_frames)
        return box_shape_from_box_angles(angles)

def box_lengths_from_box_vectors(box):

    unit = puw.get_unit(box)
    n_frames = box.shape[0]
    tmp_box =  np.asfortranarray(puw.get_value(box), dtype='float64')
    lengths = libbox.length_edges_box(tmp_box, n_frames)
    lengths = np.ascontiguousarray(lengths, dtype='float64')
    del(tmp_box)

    return lengths.round(6)*unit

def box_angles_from_box_vectors(box):

    n_frames = box.shape[0]
    tmp_box =  np.asfortranarray(puw.get_value(box), dtype='float64')
    angles = libbox.angles_box(tmp_box, n_frames)
    angles = np.ascontiguousarray(angles, dtype='float64')
    del(tmp_box)

    return puw.quantity(angles.round(6), 'degrees')

def box_vectors_from_box_lengths_and_angles(lengths, angles):

    lengths=digest_box_lengths(lengths)
    angles=digest_box_angles(angles)

    units = puw.get_unit(lengths)
    lengths_value = puw.get_value(lengths)
    angles_value = puw.get_value(angles, to_unit='degrees')
    lengths_value =  np.asfortranarray(lengths_value, dtype='float64')
    angles_value =  np.asfortranarray(angles_value, dtype='float64')
    n_frames = lengths.shape[0]

    box = libbox.lengths_and_angles_to_box(lengths_value, angles_value, n_frames)
    box = np.ascontiguousarray(box, dtype='float64').round(6)*units

    del(lengths_value, angles_value)

    return box

def box_volume_from_box_vectors(box):

    if box is not None:
        units = puw.get_unit(box)
        value = puw.get_value(box)
        volume = np.linalg.det(value)*units**3
    else:
        volume = None

    return volume

#def minimum_image_convention(item, selection='all', reference_selection=None,
#                             reference_coordinates=None, center_of_selection='geometrical_center',
#                             center_of_reference_selection='geometrical_center', frame_indices='all',
#                             syntaxis='MDTraj', engine='MolSysMT'):
#
#    from molsysmt import convert, select, get, duplicate
#    from molsysmt import set as _set
#    from molsysmt.tools.math import serialized_lists
#    from molsysmt.centers import geometrical_center
#
#    n_atoms, n_frames = get(item, n_atoms=True, n_frames=True)
#    atom_indices = select(item, selection=selection, syntaxis=syntaxis)
#    n_atom_indices = len(atom_indices)
#    frame_indices = _digest_frame_indices(item, frame_indices)
#    n_frame_indices = len(frame_indices)
#
#    engine = _digest_engines(engine)
#    form_in, _ = _digest_forms(item, engine)
#    tmp_item = duplicate(item)
#
#    if engine=='MolSysMT':
#
#        if reference_coordinates is None:
#            if center_of_reference_selection == 'geometrical_center':
#                reference_coordinates = geometrical_center(tmp_item, selection=reference_selection,
#                                                        frame_indices=frame_indices, syntaxis=syntaxis, engine=engine)
#
#        molecules = get(tmp_item, molecules=True)
#
#        if selection not in [None, 'all']:
#            working_molecules = []
#            for molecule in molecules:
#                if len(_np.intersect1d(molecule, atom_indices)):
#                    working_molecules.append(molecule)
#            molecules=working_molecules
#
#        molecules_serialized = serialized_lists(molecules, dtype='int64')
#
#        if center_of_selection == 'geometrical_center':
#            centers_molecules = geometrical_center(tmp_item, selection_groups=molecules,
#                    frame_indices=frame_indices, syntaxis=syntaxis, engine=engine)
#
#        coordinates, box, box_shape = get(tmp_item, coordinates=True, box=True, box_shape=True, frame_indices='all')
#
#        units = puw.get_unit(coordinates)
#        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
#        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates), dtype='float64')
#        box = np.asfortranarray(puw.get_value(box), dtype='float64')
#        orthogonal = 0
#        if box_shape=='cubic': orthogonal = 1
#
#        libbox.minimum_image_convention(coordinates, reference_coordinates, centers_molecules,
#                molecules_serialized.indices, molecules_serialized.values,
#                molecules_serialized.starts, frame_indices, box, orthogonal,
#                n_frames, n_atoms, molecules_serialized.n_indices, molecules_serialized.n_values,
#                n_frame_indices)
#
#        coordinates=np.ascontiguousarray(coordinates)*units
#
#        _set(tmp_item, coordinates=coordinates)
#
#        del(coordinates, box, length_units)
#        del(molecules, molecules_serialized)
#
#        return tmp_item
#
#    else:
#
#        raise NotImplementedError

#def keep_compact_molecules_in_pbc(item, selection='all', frame_indices='all', syntaxis='MDTraj', engine='MolSysMT'):
#
#    from molsysmt import convert, select, get, duplicate
#    from molsysmt import set as _set
#    from molsysmt.tools.math import serialized_lists
#
#    n_atoms, n_frames = get(item, n_atoms=True, n_frames=True)
#    atom_indices = select(item, selection=selection, syntaxis=syntaxis)
#    n_atom_indices = len(atom_indices)
#    frame_indices = _digest_frame_indices(item, frame_indices)
#    n_frame_indices = len(frame_indices)
#
#    engine = _digest_engines(engine)
#    form_in, _ = _digest_forms(item, engine)
#    tmp_item = duplicate(item)
#
#    if engine=='MolSysMT':
#
#        molecules = get(tmp_item, molecules=True)
#
#        if selection not in [None, 'all']:
#            working_molecules = []
#            for molecule in molecules:
#                if len(_np.intersect1d(molecule, atom_indices)):
#                    working_molecules.append(molecule)
#            molecules=working_molecules
#
#        molecules_serialized = serialized_lists(molecules, dtype='int64')
#
#        bonded_atoms = get(tmp_item, target='atom', indices=atom_indices, bonded_atoms=True)
#        bonded_atoms_serialized = serialized_lists(bonded_atoms, dtype='int64')
#
#        coordinates, box, box_shape = get(tmp_item, coordinates=True, box=True, box_shape=True, frame_indices='all')
#
#        units = puw.get_unit(coordinates)
#        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
#        box = np.asfortranarray(puw.get_value(box), dtype='float64')
#        orthogonal = 0
#        if box_shape=='cubic': orthogonal = 1
#
#        libbox.unwrap(coordinates, molecules_serialized.indices, molecules_serialized.values, molecules_serialized.starts,
#                       bonded_atoms_serialized.indices, bonded_atoms_serialized.values, bonded_atoms_serialized.starts,
#                       frame_indices, box, orthogonal, n_frames, n_atoms,
#                       molecules_serialized.n_indices, molecules_serialized.n_values,
#                       bonded_atoms_serialized.n_indices, bonded_atoms_serialized.n_values,
#                       n_frame_indices)
#
#        coordinates=_np.ascontiguousarray(coordinates)*units
#
#        _set(tmp_item, coordinates=coordinates)
#
#        del(coordinates, box, length_units)
#        del(molecules, molecules_serialized, bonded_atoms, bonded_atoms_serialized)
#
#        return tmp_item
#
#    else:
#
#        raise NotImplementedError

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

            from molsysmt import get_center
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

def wrap_to_mic(molecular_system, selection='all', frame_indices='all',
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

            from molsysmt import get_center
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

        libbox.wrap_mic(coordinates, center, box, orthogonal, n_atoms, n_frames)

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


