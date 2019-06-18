import numpy as _np

class serialized_lists():

    self.values = None
    self.starts = None
    self.n_values = None
    self.n_lists = None

    def __init__ (list_of_lists, fortran=False, dtype=None):

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

