import numpy as _np

def serialize_list_of_lists(list_of_lists, fortran=False, dtype=None):

    vect_starts = []
    jj = 0
    for ii in list_of_lists:
        vect_starts.append(jj)
        jj+=len(ii)
    vect_starts.append(jj)

    vect_all = _np.concatenate(list_of_lists)

    if asfortranarray:
        vect_all = _np.asfortranarray(vect_all)
        vect_starts = _np.asfortranarray(vect_starts)

    if dtype is not None:
        vect_all = _np.astype(vect_all, dtype)
        vect_starts = _np.astype(vect_starts, dtype)

    return vect_all, vect_starts

