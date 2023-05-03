import numpy as np
import numba as nb
import math


@nb.njit(nb.types.Tuple((nb.int64[:],nb.int64[:]))(nb.int64[:]))
def serie_to_chunks (serie):

    gaps = np.where((serie[1:]-serie[:-1])>1)
    offset = 0
    starts = []
    chunk_size = []
    for ii in gaps[0]:
        chunk_size.append(ii+1-offset)
        starts.append(serie[offset])
        offset = ii+1
    chunk_size.append(len(serie)-offset)
    starts.append(serie[offset])

    starts=np.asarray(starts)
    chunk_size=np.asarray(chunk_size)

    return starts, chunk_size


@nb.njit(nb.int64[:](nb.int64[:],nb.int64[:]))
def chunks_to_serie (starts, chunk_size):

    shape=np.sum(chunk_size)
    output = np.empty((shape),dtype=nb.int64)

    counter=0
    for ii,jj in zip(starts, chunk_size):
        for kk in range(jj):
            output[counter]=ii+kk
            counter+=1

    return output


class serialized_lists():

    def __init__ (self, item=None, dtype=None):

        self.values = None
        self.starts = None
        self.indices = None
        self.n_values = None
        self.n_indices = None

        if type(item) is list or type(item) is np.ndarray:

            """
            item = [[3,4,5],[1,10],[3,4,6,7],[8],[2,9,1]]
            serialized_item = serialized_lists(item)

            serialized_item.values = [3,4,5,1,10,3,4,6,7,8,1,2,9]
            serialized_item.starts = [0,3,5,9,10,13]
            serialized_item.indices = [0,1,2,3,4]
            serialized_item.n_values = 13
            serialized_item.n_indices = 5
            """

            aux_item = nb.typed.List([nb.typed.List(ii) for ii in item])

            self.starts, self.values = _jit_serialize(aux_item)
            self.indices = np.arange(len(item))

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

            self.indices = np.sort(list(item.keys()))

            aux_item = nb.typed.List([nb.typed.List(sorted(item[ii])) for ii in self.indices])

            self.starts, self.values = _jit_serialize(aux_item)

            self.n_values = self.values.shape[0]
            self.n_indices = self.indices.shape[0]

            self.n_values = self.values.shape[0]
            self.n_indices = self.indices.shape[0]


@nb.njit(nb.types.UniTuple(nb.int64[:], 2)(nb.types.ListType(nb.types.ListType(nb.int64))))
def _jit_serialize(item):

    n_values=0
    n_starts=0
    for segment in item:
        n_values+=len(segment)
        n_starts+=1

    values = np.empty((n_values), dtype=nb.int64)
    starts = np.empty((n_starts+1), dtype=nb.int64)

    counter=0
    for ii,segment in enumerate(item):
        starts[ii]=counter
        for jj in sorted(segment):
            values[counter]=jj
            counter+=1

    starts[-1]=counter

    return starts, values


@nb.njit(nb.int64[:](nb.int64[:]))
def occurrence_order(serie):


    output = np.zeros(serie.shape[0], dtype=nb.int64)

    aux={}
    in_aux = 0

    for ii in serie:
        if not ii in aux:
            aux[ii]=in_aux
            in_aux+=1

    for ii, jj in enumerate(serie):
        output[ii]=aux[jj]

    return output

