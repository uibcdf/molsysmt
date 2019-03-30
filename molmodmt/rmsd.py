from mdtraj import rmsd as _mdtraj_rmsd
from mdtraj import lprmsd as _mdtraj_lprmsd
from numpy import asarray as _asarray, arange as _arange
from .multitool import get_form as _get_form, select as _select, convert as _convert
from .utils.digest_inputs import _comparison_two_systems as _digest_comparison_two_systems

def rmsd(ref_item=None, item=None,
         ref_selection=None, ref_frame=0,
         selection='name CA', frame='All',
         pbc=False, parallel=False, precentered=False, engine='mdtraj'):

    ref_item, ref_atom_indices, ref_frame_indices, item, atom_indices, frame_indices = \
            _digest_input_two_systems(ref_item, ref_selection, ref_frame, item, selection, frame)

    if engine=='native':
        raise NotImplementedError

    elif engine=='mdtraj':

        mdtraj_ref_item=_convert(ref_item,'mdtraj.Trajectory')
        mdtraj_item = _convert(item,'mdtraj.Trajectory')
        return _mdtraj_rmsd(mdtraj_item, mdtraj_ref_item, frame=ref_frame_indices,
                            ref_atom_indices=ref_atom_indices, atom_indices=atom_indices, parallel=parallel, precentered=precentered)

def least_rmsd(ref_item=None, item=None,
        ref_selection=None, ref_frame=0,
        selection='name CA', frame='All',
        pbc=False, parallel=False, precentered=False, engine='mdtraj'):

    ref_item, ref_atom_indices, ref_frame_indices, item, atom_indices, frame_indices = \
            _digest_input_two_systems(ref_item, ref_selection, ref_frame, item, selection, frame)

    if engine=='native':
        raise NotImplementedError

    elif engine=='mdtraj':

        mdtraj_ref_item=_convert(ref_item,'mdtraj.Trajectory')
        mdtraj_item = _convert(item,'mdtraj.Trajectory')
        return _mdtraj_lprmsd(mdtraj_item, mdtraj_ref_item, frame=ref_frame_indices,
                              ref_atom_indices=ref_atom_indices, atom_indices=atom_indices, parallel=parallel, precentered=precentered)

def least_rmsd_fit(ref_item=None, item=None,
        ref_selection=None, ref_frame=0,
        selection='backbone', frame='All',
        pbc=False, parallel=False, in_place=False, engine='mdtraj'):

    ref_item, ref_atom_indices, ref_frame_indices, item, atom_indices, frame_indices = \
    _digest_comparison_two_systems(ref_item, ref_selection, ref_frame, item, selection, frame)

    if engine=='native':
        raise NotImplementedError

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

