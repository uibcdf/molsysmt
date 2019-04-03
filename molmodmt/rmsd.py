from mdtraj import rmsd as _mdtraj_rmsd
from mdtraj import lprmsd as _mdtraj_lprmsd
import numpy as _np
from .lib import rmsd as _librmsd
from .multitool import get_form as _get_form, select as _select, convert as _convert
from .utils.digest_inputs import _comparison_two_systems as _digest_comparison_two_systems

def rmsd(ref_item=None, ref_selection=None, ref_frame=0, item=None, selection='backbone',
         parallel=False, precentered=False, engine='molmodmt'):

    ref_item, ref_atom_indices, ref_frame_indices, \
    item, atom_indices, frame_indices,\
    single_item, diff_selection = _digest_comparison_two_systems(ref_item, ref_selection, ref_frame,
                                                                 item, selection, 'all')

    if engine=='molmodmt':

        tmp_item = item
        tmp_ref_item = ref_item

        tmp_item.coordinates=_np.asfortranarray(tmp_item.coordinates,dtype='float64')
        tmp_ref_item.coordinates=_np.asfortranarray(tmp_ref_item.coordinates,dtype='float64')
        rmsd_val=_librmsd.rmsd(tmp_ref_item.coordinates[ref_frame,:,:], ref_atom_indices,
                               tmp_item.coordinates, atom_indices,
                               tmp_ref_item.n_atoms, ref_atom_indices.shape[0],
                               tmp_item.n_frames, tmp_item.n_atoms, atom_indices.shape[0])
        return rmsd_val


    elif engine=='mdtraj':

        mdtraj_ref_item=_convert(ref_item,'mdtraj.Trajectory')
        mdtraj_item = _convert(item,'mdtraj.Trajectory')
        rmsd_val = _mdtraj_rmsd(mdtraj_item, mdtraj_ref_item, frame=ref_frame_indices,
                                ref_atom_indices=ref_atom_indices, atom_indices=atom_indices,
                                parallel=parallel, precentered=precentered)
        return rmsd_val

    else:
        raise NotImplementedError

def least_rmsd(ref_item=None, ref_selection=None, ref_frame=0, item=None, selection='backbone',
               parallel=False, precentered=False, engine='molmodmt'):

    ref_item, ref_atom_indices, ref_frame_indices, \
    item, atom_indices, frame_indices,\
    single_item, diff_selection = _digest_comparison_two_systems(ref_item, ref_selection, ref_frame,
                                                                 item, selection, 'all')

    if engine=='molmodmt':

        tmp_item = item
        tmp_ref_item = ref_item

        tmp_item.coordinates=_np.asfortranarray(tmp_item.coordinates,dtype='float64')
        rmsd_val = _np.array(tmp_item.n_frames,dtype=float)
        tmp_ref_item.coordinates=_np.asfortranarray(tmp_ref_item.coordinates,dtype='float64')
        rmsd_val=_librmsd.least_rmsd(tmp_ref_item.coordinates[ref_frame,:,:], ref_atom_indices,
                                     tmp_item.coordinates, atom_indices,
                                     tmp_ref_item.n_atoms, ref_atom_indices.shape[0],
                                     tmp_item.n_frames, tmp_item.n_atoms, atom_indices.shape[0])

        return rmsd_val

    elif engine=='mdtraj':

        mdtraj_ref_item=_convert(ref_item,'mdtraj.Trajectory')
        mdtraj_item = _convert(item,'mdtraj.Trajectory')
        rmsd_val = _mdtraj_lprmsd(mdtraj_item, mdtraj_ref_item, frame=ref_frame_indices,
                              ref_atom_indices=ref_atom_indices, atom_indices=atom_indices, parallel=parallel, precentered=precentered)
        return rmsd_val

    else:

        raise NotImplementedError

def least_rmsd_fit(ref_item=None, ref_selection=None, ref_frame=0, item=None, selection='backbone',
                   parallel=False, in_place=True, engine='molmodmt'):

    ref_item, ref_atom_indices, ref_frame_indices, \
    item, atom_indices, frame_indices,\
    single_item, diff_selection = _digest_comparison_two_systems(ref_item, ref_selection, ref_frame,
                                                                 item, selection, 'all')

    if engine=='molmodmt':

        tmp_item = item
        tmp_ref_item = ref_item

        tmp_item.coordinates=_np.asfortranarray(tmp_item.coordinates,dtype='float64')
        tmp_ref_item.coordinates=_np.asfortranarray(tmp_ref_item.coordinates,dtype='float64')
        _librmsd.least_rmsd_fit(tmp_ref_item.coordinates[ref_frame,:,:], ref_atom_indices,
                                tmp_item.coordinates, atom_indices,
                                tmp_ref_item.n_atoms, ref_atom_indices.shape[0],
                                tmp_item.n_frames, tmp_item.n_atoms, atom_indices.shape[0])

        item.coordinates=_np.ascontiguousarray(tmp_item.coordinates)
        pass

    elif engine=='mdtraj':

        output_form = _get_form(item)
        mdtraj_ref_item=_convert(ref_item,'mdtraj.Trajectory')
        mdtraj_item = _convert(item,'mdtraj.Trajectory')
        mdtraj_item.superpose(mdtraj_ref_item,frame=ref_frame_indices,atom_indices=atom_indices,ref_atom_indices=ref_atom_indices,parallel=parallel)

        if in_place:
            item = _convert(mdtraj_item,output_form)
            pass
        else:
            return _convert(mdtraj_item,output_form)

    else:

        raise NotImplementedError
