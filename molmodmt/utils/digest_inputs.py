from numpy import asarray as _asarray, arange as _arange
import numpy as _np
from molmodmt import get_form as _get_form, get_shape as _get_shape, select as _select, convert as _convert
from .exceptions import *

def _one_system(item1=None, selection1=None, frame1=None, engine=None):

    atom_indices1=None
    frame_indices1=None

    if engine is not None:
        tmp_item1=_convert(item1,engine)
    else:
        tmp_item1=item1

    if selection1 is not None:
        atom_indices1 = _select(tmp_item1,selection1)

    frame_indices1 = _frameslist(tmp_item1,frame1)

    return tmp_item1, atom_indices1, frame_indices1

def _frameslist(item=None,frame=None):

    if frame is None:
        tmp_frameslist = _asarray([0])
    elif type(frame) == int:
        tmp_frameslist = _asarray([frame])
    elif type(frame) == list:
        tmp_frameslist = _asarray(frame)
    elif type(frame) == _np.ndarray:
        tmp_frameslist = frame
    elif frame == 'all':
        tmp_frameslist = _arange(_get_shape(item)[0])

    return tmp_frameslist

def _coordinates(item=None, selection=None, frame=None, engine='molmodmt'):

    if engine=='molmodmt':
        tmp_atomslist=_select(item,selection)
        tmp_frameslist=_frameslist(item,frame)
        tmp_coordinates = item.trajectory.coordinates[tmp_frameslist,tmp_atomslist,:]
        tmp_natoms = tmp_atomslist.shape[0]
        tmp_nframes = tmp_frameslist.shape[0]
        if tmp_natoms==1 and tmp_nframes==1:
            tmp_coordinates = tmp_coordinates.reshape(1,1,3)
        elif tmp_natoms==1:
            tmp_coordinates = tmp_coordinates.reshape(tmp_nframes,1,3)
        elif tmp_nframes==1:
            tmp_coordinates = tmp_coordinates.reshape(1,tmp_natoms,3)

        return tmp_coordinates

    else:
        raise NotImplementedError(NotImplementedMessage)

def _comparison_two_systems(item1=None, selection1=None, frame1=None,
                            item2=None, selection2=None, frame2=None,
                            engine=None):

    single_item = False
    diff_selection = True
    atom_indices1=None
    atom_indices2=None
    frame_indices1=None
    frame_indices2=None

    if item1 is None and item2 is None:
        raise BadCallError(BadCallMessage)

    if item1 is None or item2 is None:
        single_item = True
        if item1 is None:
            item1 = item2
        else:
            item2 = item1

    if engine is not None:
        tmp_item1=_convert(item1,engine)
        tmp_item2=_convert(item2,engine)
    else:
        tmp_item1=item1
        tmp_item2=item2

    if selection1 is not None:
        atom_indices1 = _select(tmp_item1,selection1)

    if selection2 is not None:
        atom_indices2 = _select(tmp_item2,selection2)

    if selection1 is None and selection2 is None:

        atom_indices1= None
        atom_indices2= None

    elif selection1 is None or selection2 is None:
        if single_item is True:
            diff_selection = False
            if selection1 is None:
                atom_indices1 = atom_indices2
            else:
                atom_indices2 = atom_indices1
        else:
            if selection1 is None:
                atom_indices1 = _select(tmp_item1,selection2)
            else:
                atom_indices2 = _select(tmp_item2,selection1)

    frame_indices1 = _frameslist(tmp_item1,frame1)
    frame_indices2 = _frameslist(tmp_item2,frame2)

    return tmp_item1, atom_indices1, frame_indices1, \
           tmp_item2, atom_indices2, frame_indices2, \
           single_item, diff_selection

