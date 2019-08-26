import numpy as _np

class serialized_lists():

    def __init__ (self, list_of_lists=None, fortran=False, dtype=None):

        self.values = None
        self.starts = None
        self.n_values = None
        self.n_lists = None

        self.values= _np.concatenate(list_of_lists)

        self.starts= []
        jj = 0
        for ii in list_of_lists:
            self.starts.append(jj)
            jj+=len(ii)
        self.starts.append(jj)

        if fortran:
            self.values = _np.asfortranarray(self.values)
            self.starts = _np.asfortranarray(self.starts)

        if dtype is not None:
            self.values = _np.astype(self.values, dtype)

        self.starts = _np.array(self.starts, dtype=int)

        self.n_values = self.values.shape[0]
        self.n_lists = self.starts.shape[0]-1

def serie_to_chunks (serie):

    np_serie = _np.array(serie)
    gaps = _np.where((np_serie[1:]-np_serie[:-1])>1)
    offset = 0
    starts = []
    chunk_size = []
    for ii in gaps[0]:
        chunk_size.append(ii+1-offset)
        starts.append(serie[offset])
        offset = ii+1
    chunk_size.append(len(serie)-offset)
    starts.append(serie[offset])

    return starts, chunk_size

