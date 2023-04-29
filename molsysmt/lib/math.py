import numpy as np
import numba as nb
import math


@nb.njit(nb.float64[:,:](nb.float64[:,:]))
def inverse_matrix_3x3(m):

    inv = np.zeros(m.shape, dtype=nb.float64)

    inv[0,0]=1.0/m[0,0]
    inv[1,1]=1.0/m[1,1]
    inv[2,2]=1.0/m[2,2]

    inv[1,0]=-m[1,0]/(m[0,0]*m[1,1])
    inv[2,0]=(m[1,0]*m[2,1]-m[2,0]*m[1,1])/(m[0,0]*m[1,1]*m[2,2])
    inv[2,1]=-m[2,1]/(m[1,1]*m[2,2])

    return inv

@nb.njit(nb.float64[:](nb.float64[:,:],nb.float64[:]))
def matmul(m,v):
    o = np.zeros(m.shape[0], nb.float64)
    for ii in range(m.shape[0]):
        for jj in range(m.shape[1]):
            o[ii]+=m[ii,jj]*v[jj]
    return o

@nb.njit(nb.float64[:](nb.float64[:,:],nb.float64[:]))
def transpmatmul(m,v):
    o = np.zeros(m.shape[1], nb.float64)
    for jj in range(m.shape[0]):
        for ii in range(m.shape[1]):
            o[ii]+=m[jj,ii]*v[jj]
    return o

@nb.njit(nb.float64(nb.float64[:], nb.float64[:]))
def dot_product(a, b):

    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]


@nb.njit(nb.float64[:](nb.float64[:], nb.float64[:]))
def cross_product(a, b):

    output=np.empty((3), dtype=nb.float64)

    output[0]=a[1]*b[2]-a[2]*b[1]
    output[1]=-a[0]*b[2]+a[2]*b[0]
    output[2]=a[0]*b[1]-a[1]*b[0]

    return output

@nb.njit(nb.types.Tuple((nb.int64[:],nb.int64[:]))(nb.int64[:]))
def serie_to_chunks (serie):

    gaps = np.where((serie[1:]-serie[:-1])>1)
    offset = 0
    starts = []
    chunk_size = []
    print(gaps)
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

@nb.njit(nb.void(nb.float64[:], nb.float64[:], nb.float64))
def rodrigues_rotation(vector, unit_vector, angle):

    aux_ang = math.radians(angle)

    cosa = math.cos(aux_ang)
    sina = math.sin(aux_ang)

    aux1 = vector*cosa
    aux2 = cross_product(unit_vector, vector)
    aux2 = aux2*sina
    aux3 = dot_product(unit_vector, vector)*(1.0-cosa)*unit_vector

    vector = aux1+aux2+aux3

    pass

@nb.njit(nb.float64[:,:](nb.float64[:]))
def quaternion_to_rotation_matrix(q):

    q0, q1, q2, q3 = q

    U=np.empty((3,3), dtype=float)

    q00=2*q0*q0
    q11=2*q1*q1
    q22=2*q2*q2
    q33=2*q3*q3

    q01=2*q0*q1
    q02=2*q0*q2
    q03=2*q0*q3
    q12=2*q1*q2
    q13=2*q1*q3
    q23=2*q2*q3

    U[0,0]=q00+q11-1.0
    U[1,1]=q00+q22-1.0
    U[2,2]=q00+q33-1.0

    U[0,1]=q12-q03
    U[1,0]=q12+q03

    U[0,2]=q13+q02
    U[2,0]=q13-q02

    U[1,2]=q23-q01
    U[2,1]=q23+q01

    return U

@nb.njit(nb.int64(nb.int64[:]))
def occurrence_order(serie):


    output = np.zeros(serie.shape[0], dtype=nb.int64)

    aux={}
    in_aux = 0

    for ii in component_indices:
        if not ii in aux:
            aux[ii]=in_aux
            in_aux+=1

    for ii, jj in enumerate(component_indices):
        output[ii]=aux[jj]

    pass


