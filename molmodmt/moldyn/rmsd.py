from mdtraj import rmsd as _mdtraj_rmsd
from numpy import asarray as _asarray, arange as _arange
from .multitool import get_form as _get_form, get_shape as _get_shape, select as _select, convert as _convert

def _digest_inputs(ref_item=None, ref_selection=None, ref_frame=None, item=None,
        selection=None, frame=None):

    single_item = False
    ref_atom_indices=None
    ref_frame_indices=None
    atom_indices=None
    frame_indices=None

    if ref_item is None and item is None:
        raise Exception('Providing ref_item and/or item is mandatory')

    if ref_selection is None and selection is None:
        raise Exception('Providing ref_selection and/or selection is mandatory')

    if ref_item is None or item is None:
        single_item = True
        if ref_item is None:
            ref_item = item
        else:
            item = ref_item

    if ref_selection is not None:
        ref_atom_indices = _select(ref_item,ref_selection)

    if selection is not None:
        atom_indices = _select(item,selection)

    if ref_selection is None or selection is None:
        if single_item is True:
            if ref_selection is None:
                ref_atom_indices = atom_indices
            else:
                atom_indices = ref_atom_indices
        else:
            if ref_selection is None:
                ref_atom_indices = _select(ref_item,selection)
            else:
                atom_indices = _select(item,ref_selection)

    if ref_frame is None:
        ref_frame_indices = _asarray([0])
    elif type(ref_frame) == int:
        ref_frame_indices = _asarray([ref_frame])
    elif type(ref_frame) == list:
        ref_frame_indices = _asarray(ref_frame)
    elif ref_frame.capitalize() == 'All':
        ref_frame_indices = _arange(_get_shape(ref_item)[0])

    if frame is None:
        frame_indices = _asarray([0])
    elif type(frame) == int:
        frame_indices = _asarray([frame])
    elif type(frame) == list:
        frame_indices = _asarray(frame)
    elif frame.capitalize() == 'All':
        frame_indices = _arange(_get_shape(item)[0])

    return ref_item, ref_atom_indices, ref_frame_indices, item, atom_indices, frame_indices

#def rmsd(ref_item=None, ref_select='All', ref_frame=0,
#         item=None, select=None, frame='All',
#         pbc=False, parallel=False, engine='native'):
#
#    single_system = _complete_ref(ref_system, ref_trajectory, ref_topology, ref_frame_indices, ref_selection, ref_atom_indices,
#                                  system, trajectory, topology, frame_indices, selection, atom_indices)
#
#    native_system = import_system(system,trajectory,topology)
#
#    if single_system:
#        ref_native_system = native_system
#    else:
#        ref_native_system = import_system(ref_system,ref_trajectory,ref_topology)
#
#    if engine=='self':
#
#        _not_implemented(); pass
#
#    pass

def least_rmsd(ref_item=None, item=None,
        ref_selection=None, ref_frame=0,
        selection='name CA', frame='All',
        pbc=False, parallel=False, precentered=False, engine='mdtraj'):

    ref_item, ref_atom_indices, ref_frame_indices, item, atom_indices, frame_indices = _digest_inputs(ref_item, ref_selection, ref_frame, item, selection, frame)

    if engine=='native':
        raise NotImplementedError

    elif engine=='mdtraj':

        mdtraj_ref_item=_convert(ref_item,'mdtraj.Trajectory')
        mdtraj_item = _convert(item,'mdtraj.Trajectory')
        return _mdtraj_rmsd(mdtraj_item, mdtraj_ref_item, frame=ref_frame_indices,
                            ref_atom_indices=ref_atom_indices, atom_indices=atom_indices, parallel=parallel, precentered=precentered)

def superpose(ref_item=None, item=None,
        ref_selection=None, ref_frame=0,
        selection='name CA', frame='All',
        pbc=False, parallel=False, precentered=False, in_place=True, engine='mdtraj'):

    return least_rmsd_fit(ref_item, item, ref_selection, ref_frame, selection, frame, pbc,
                          parallel, precentered, in_place, engine)


def least_rmsd_fit(ref_item=None, item=None,
        ref_selection=None, ref_frame=0,
        selection='name CA', frame='All',
        pbc=False, parallel=False, precentered=False, in_place=True, engine='mdtraj'):

    ref_item, ref_atom_indices, ref_frame_indices, item, atom_indices, frame_indices = _digest_inputs(ref_item, ref_selection, ref_frame, item, selection, frame)

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

