import numpy as _np
from copy import deepcopy as _deepcopy
from .lib import rmsd as _librmsd
from .multitool import get_form as _get_form, select as _select, convert as _convert
from .utils.digest_inputs import _comparison_two_systems as _digest_comparison_two_systems

def rmsd(ref_item=None, ref_selection=None, ref_frame=0, item=None, selection='backbone',
         parallel=False, precentered=True, syntaxis='mdtraj', engine='molmodmt'):

    if item is None:
        in_form=_get_form(ref_item)
        output_item=ref_item
    else:
        in_form=_get_form(item)
        output_item=item

    if engine=='molmodmt':
        x_form='molmodmt.Trajectory'
    elif engine=='mdtraj':
        x_form='mdtraj.Trajectory'


    tmp_ref_item, ref_atom_indices, ref_frame_indices, \
    tmp_item, atom_indices, frame_indices,\
    single_item, diff_selection = _digest_comparison_two_systems(ref_item, ref_selection, ref_frame,
                                                                 item, selection, 'all',
                                                                 form=x_form, syntaxis=syntaxis)

    if engine=='molmodmt':
        tmp_coordinates=_np.asfortranarray(tmp_item.coordinates,dtype='float64')
        tmp_ref_coordinates=_np.asfortranarray(tmp_ref_item.coordinates[ref_frame,:,:],dtype='float64')
        rmsd_val=_librmsd.rmsd(tmp_ref_coordinates, ref_atom_indices,
                               tmp_coordinates, atom_indices,
                               tmp_ref_item.n_atoms, ref_atom_indices.shape[0],
                               tmp_item.n_frames, tmp_item.n_atoms, atom_indices.shape[0])
        return rmsd_val


    elif engine=='mdtraj':
        from mdtraj import rmsd as _mdtraj_rmsd
        rmsd_val = _mdtraj_rmsd(tmp_item, tmp_ref_item, frame=ref_frame_indices,
                                ref_atom_indices=ref_atom_indices, atom_indices=atom_indices,
                                parallel=parallel, precentered=precentered)
        return rmsd_val

    else:
        raise NotImplementedError

def least_rmsd_fit_2(ref_item=None, item=None,
                   ref_selection=None, selection='backbone',
                   ref_frame_index=0, frame_indices='all',
                   engine='molmodmt',
                   parallel=True, syntaxis='mdtraj'):

    if item is None:
        in_form=_get_form(ref_item)
        item=ref_item
    else:
        in_form=_get_form(item)

    if engine=='molmodmt':
        x_form='molmodmt.MolMod'
    elif engine=='mdtraj':
        x_form='mdtraj.Trajectory'

    tmp_ref_item, ref_atom_indices, ref_frame_indices, \
    tmp_item, atom_indices, frame_indices,\
    single_item, diff_selection = _digest_comparison_two_systems(ref_item, ref_selection,
                                                                 ref_frame_index,
                                                                 item, selection, frame_indices,
                                                                 form=x_form, syntaxis=syntaxis)
    if engine=='molmodmt':

        tmp_coordinates=_np.asfortranarray(tmp_item.coordinates,dtype='float64')
        tmp_ref_coordinates=_np.asfortranarray(tmp_ref_item.coordinates[ref_frame,:,:],dtype='float64')
        _librmsd.least_rmsd_fit(tmp_ref_coordinates, ref_atom_indices,
                                tmp_coordinates, atom_indices,
                                tmp_ref_item.n_atoms, ref_atom_indices.shape[0],
                                tmp_item.n_frames, tmp_item.n_atoms, atom_indices.shape[0])

        if in_form==x_form:
            tmp_item.coordinates=_np.ascontiguousarray(tmp_coordinates)
        elif in_form=='molmodmt.MolMod':
            tmp_item.trajectory.coordinates=_np.ascontiguousarray(tmp_coordinates)
        else:
            tmp_item.coordinates=_np.ascontiguousarray(tmp_coordinates)
            tmp_item=_convert(tmp_item,in_form)

        pass

    elif engine=='mdtraj':

        tmp_item.superpose(tmp_ref_item,frame=ref_frame_indices,atom_indices=atom_indices,ref_atom_indices=ref_atom_indices,parallel=parallel)

        if in_form==x_form:
            item=tmp_item
        elif in_form=='molmodmt.Trajectory':
            item._import_mdtraj_data(tmp_item)
        elif in_form=='molmodmt.MolMod':
            item.trajectory._import_mdtraj_data(tmp_item)
        else:
            item=_convert(tmp_item,in_form)

    else:

        raise NotImplementedError

def least_rmsd_fit(ref_item=None, item=None,
                   ref_selection=None, selection='backbone',
                   ref_frame_index=0, frame_indices='all',
                   engine='molmodmt',
                   parallel=True, syntaxis='mdtraj'):

    if item is None:
        in_form=_get_form(ref_item)
        item=ref_item
    else:
        in_form=_get_form(item)

    if engine=='molmodmt':
        x_form='molmodmt.MolMod'
    elif engine=='mdtraj':
        x_form='mdtraj.Trajectory'

    tmp_ref_item, ref_atom_indices, ref_frame_indices, \
    tmp_item, atom_indices, frame_indices,\
    single_item, diff_selection = _digest_comparison_two_systems(ref_item, ref_selection,
                                                                 ref_frame_index,
                                                                 item, selection, frame_indices,
                                                                 form=x_form, syntaxis=syntaxis)
    if engine=='molmodmt':

        tmp_coordinates=_np.asfortranarray(tmp_item.coordinates,dtype='float64')
        tmp_ref_coordinates=_np.asfortranarray(tmp_ref_item.coordinates[ref_frame,:,:],dtype='float64')
        _librmsd.least_rmsd_fit(tmp_ref_coordinates, ref_atom_indices,
                                tmp_coordinates, atom_indices,
                                tmp_ref_item.n_atoms, ref_atom_indices.shape[0],
                                tmp_item.n_frames, tmp_item.n_atoms, atom_indices.shape[0])

        if in_form==x_form:
            tmp_item.coordinates=_np.ascontiguousarray(tmp_coordinates)
        elif in_form=='molmodmt.MolMod':
            tmp_item.trajectory.coordinates=_np.ascontiguousarray(tmp_coordinates)
        else:
            tmp_item.coordinates=_np.ascontiguousarray(tmp_coordinates)
            tmp_item=_convert(tmp_item,in_form)

        pass

    elif engine=='mdtraj':

        tmp_item.superpose(tmp_ref_item,frame=ref_frame_indices,atom_indices=atom_indices,ref_atom_indices=ref_atom_indices,parallel=parallel)

        if in_form==x_form:
            item=tmp_item
        elif in_form=='molmodmt.Trajectory':
            item._import_mdtraj_data(tmp_item)
        elif in_form=='molmodmt.MolMod':
            item.trajectory._import_mdtraj_data(tmp_item)
        else:
            item=_convert(tmp_item,in_form)

    else:

        raise NotImplementedError
