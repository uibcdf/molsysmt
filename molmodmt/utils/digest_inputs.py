from numpy import asarray as _asarray, arange as _arange
from molmodmt import get_form as _get_form, get_shape as _get_shape, select as _select, convert as _convert

def _comparison_two_systems(ref_item=None, ref_selection=None, ref_frame=None,
                            item=None, selection=None, frame=None):

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

