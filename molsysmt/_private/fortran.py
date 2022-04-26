import numpy as np

def list_of_lists_to_fortran( nestedlists, dtype=None):

    if dtype is None:
        vect_all = np.asfortranarray(np.concatenate(nestedlists))
    else:
        vect_all = np.asfortranarray(np.concatenate(nestedlists),dtype=dtype)
    vect_starts = []
    jj = 0
    for ii in nestedlists:
        vect_starts.append(jj)
        jj+=len(ii)
    vect_starts.append(jj)
    if dtype is None:
        vect_starts = np.asfortranarray(vect_starts)
    else:
        vect_starts = np.asfortranarray(vect_starts, dtype=dtype)
    return vect_all, vect_starts

