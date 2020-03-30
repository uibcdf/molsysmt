import numpy as _np

class serialized_lists():

    def __init__ (self, item=None, dtype=None):

        self.values = None
        self.starts = None
        self.indices = None
        self.n_values = None
        self.n_indices = None


        if type(item) is list:

            """
            item = [[3,4,5],[1,10],[3,4,6,7],[8],[2,9,1]]
            serialized_item = serialized_lists(item)
            
            serialized_item.values = [3,4,5,1,10,3,4,6,7,8,1,2,9]
            serialized_item.starts = [0,3,5,9,10,13]
            serialized_item.indices = [0,1,2,3,4]
            serialized_item.n_values = 13
            serialized_item.n_indices = 5
            """

            self.values =  [_np.sort(ll) for ll in item]
            self.values = _np.concatenate(self.values)
            self.indices = _np.arange(len(item))
            self.starts= []
            jj = 0
            for ii in item:
                self.starts.append(jj)
                jj+=len(ii)
            self.starts.append(jj)

            self.starts = _np.array(self.starts, dtype=int)

            self.n_values = self.values.shape[0]
            self.n_indices = self.indices.shape[0]

        elif type(item) is dict:

            """
            item = {2:[3,4,5],7:[1,10],8:[3,4,6,7],3:[8],6:[2,9,1]}
            serialized_item = serialized_lists(item)
            
            item = [2:[3,4,5],3:[8],6:[2,9,1],7:[1,10],8:[3,4,6,7]]
            serialized_item.values = [3,4,5,8,1,2,9,1,10,3,4,6,7]
            serialized_item.starts = [0,3,4,7,9,13]
            serialized_item.indices = [2,3,6,7,8]
            serialized_item.n_values = 13
            serialized_item.n_indices = 5
            """

            self.indices = _np.sort(list(item.keys()))

            self.values = []
            self.starts= []
            jj = 0
            for ii in self.indices:
                self.values.append(_np.sort(item[ii]))
                self.starts.append(jj)
                jj+=len(item[ii])
            self.starts.append(jj)

            self.values = _np.concatenate(self.values)
            self.starts = _np.array(self.starts, dtype=int)

            self.n_values = self.values.shape[0]
            self.n_indices = self.indices.shape[0]

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

