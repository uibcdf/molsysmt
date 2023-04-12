import numpy as np
import numba as nb
import math



@nb.jit(nb.float64[:,:](nb.float64[:,:]), nopython=True)
def inverse_matrix_3x3(m):

    inv = np.zeros(m.shape, dtype=nb.float64)

    inv[0,0]=1.0/m[0,0]
    inv[1,1]=1.0/m[1,1]
    inv[2,2]=1.0/m[2,2]

    inv[1,0]=-m[1,0]/(m[0,0]*m[1,1])
    inv[2,0]=(m[1,0]*m[2,1]-m[2,0]*m[1,1])/(m[0,0]*m[1,1]*m[2,2])
    inv[2,1]=-m[2,1]/(m[1,1]*m[2,2])

    return inv


@nb.jit(nb.float64(nb.float64[:]), nopython=True)
def norm_vector(a):

    return math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])


@nb.jit(nb.float64(nb.float64[:]), nopython=True)
def normalize_vector(a):

    norm = math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])
    return a/norm


@nb.jit(nb.float64(nb.float64[:], nb.float64[:]), nopython=True)
def dot_product(a, b):

    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]


@nb.jit(nb.float64[:](nb.float64[:], nb.float64[:]), nopython=True)
def cross_product(a, b):

    output=np.empty((3), dtype=nb.float64)

    output[0]=a[1]*b[2]-a[2]*b[1]
    output[1]=-a[0]*b[2]+a[2]*b[0]
    output[2]=a[0]*b[1]-a[1]*b[0]

    return output


@nb.jit(nb.float64[:,:](nb.float64[:], nb.float64[:,:], nb.float64[:], nb.float64[:,:],), nopython=True)
def rotandtrans_rmsd(center_orig, U, center_ref, coors):

    dim_coors = coors.shape[0]

    new_coors=np.empty((dim_coors,3), dtype=float)

    for ii in range(dim_coors):
       new_coors[ii,:]=np.matmul(np.transpose(U),coors[ii,:]-center_orig)+center_ref

    return new_coors


@nb.jit(nb.types.Tuple((nb.int64[:],nb.int64[:]))(nb.int64[:]), nopython=True)
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


@nb.jit(nb.int64[:](nb.int64[:],nb.int64[:]), nopython=True)
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


def nb.jit(nb.types.UniTuple(nb.int64[:], 2)(nb.types.List(dtype=nb.types.List(dtype=nb.int64))), nopython=True)
def _jit_serialize(item):

    n_values=0
    n_starts=0
    for segment in item:
        n_values+=len(segment)
        n_starts+=1

    values = np.empty((n_values), dtype=int)
    starts = np.empty((n_starts+1), dtype=int)

    counter=0
    for ii,segment in enumerate(item):
        starts[ii]=counter
        for jj in sorted(segment):
            values[counter]=jj
            counter+=1

    starts[-1]=counter

    return starts, values

def nb.jit(void(nb.float64[:], nb.float64[:], nb.float64), nopython=True)
def rogrigues_rotation(vector, unit_vector, angle):

    aux_ang = math.radians(angle)

    cosa = math.cos(aux_ang)
    sina = math.sin(aux_ang)

    aux1 = vector*cosa
    aux2 = cross_product(unit_vector, vector)
    aux2 = aux2*sina
    aux3 = dot_product(unit_vector, vector)*(1.0-cosa)*unit_vector

    vector = aux1+aux2+aux3

    pass

def nb.jit(nb.float64[:,:],(nb.float64[:]), nopython=True)
def quaternion_to_rotation_matrix(q):

    q0, q1, q2, q3 = q

    U=np.empty((3,3), dtype=float)

    q00=2*q0*q0
    q11=2*q1*q1
    q22=2*q2*q2

    q01=2*q0*q1
    q02=2*q0*q2
    q12=2*q1*q2

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

