from numpy import asarray as _asarray, arange as _arange
from molmodmt import get_form as _get_form, get_shape as _get_shape, select as _select, convert as _convert
from .exceptions import *

def _comparison_two_systems(item1=None, selection1=None, frame1=None,
                            item2=None, selection2=None, frame2=None,
                            engine=None):

    single_item = False
    atom_indices1=None
    atom_indices2=None
    frame_indices1=None
    frame_indices2=None

    if item1 is None and item2 is None:
        raise BadCallError(BadCallMessage)

    if selection1 is None and selection2 is None:
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

    if selection1 is None or selection2 is None:
        if single_item is True:
            if selection1 is None:
                atom_indices1 = atom_indices2
            else:
                atom_indices2 = atom_indices1
        else:
            if selection1 is None:
                atom_indices1 = _select(tmp_item1,selection2)
            else:
                atom_indices2 = _select(tmp_item2,selection1)

    if frame1 is None:
        frame_indices1 = _asarray([0])
    elif type(frame1) == int:
        frame_indices1 = _asarray([frame1])
    elif type(frame1) == list:
        frame_indices1 = _asarray(frame1)
    elif frame1 == 'all':
        frame_indices1 = _arange(_get_shape(tmp_item1)[0])

    if frame2 is None:
        frame_indices2 = _asarray([0])
    elif type(frame2) == int:
        frame_indices2 = _asarray([frame2])
    elif type(frame2) == list:
        frame_indices2 = _asarray(frame2)
    elif frame2 == 'all':
        frame_indices2 = _arange(_get_shape(tmp_item2)[0])

    return tmp_item1, atom_indices1, frame_indices1, \
           tmp_item2, atom_indices2, frame_indices2, \
           single_item

