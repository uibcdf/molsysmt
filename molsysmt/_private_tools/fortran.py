import numpy as _np

def listoflists2fortran( nestedlists,dtype=None):

    if dtype is None:
        vect_all = _np.asfortranarray(_np.concatenate(nestedlists))
    else:
        vect_all = _np.asfortranarray(_np.concatenate(nestedlists),dtype=dtype)
    vect_starts = []
    jj = 0
    for ii in nestedlists:
        vect_starts.append(jj)
        jj+=len(ii)
    vect_starts.append(jj)
    if dtype is None:
        vect_starts = _np.asfortranarray(vect_starts)
    else:
        vect_starts = _np.asfortranarray(vect_starts,dtype=dtype)
    return vect_all, vect_starts

