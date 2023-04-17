import numpy as np
import numba as nb
import math

def dihedral_angle(vect1, vect2, vect3):

    aux1 = cross_product(vect1, vect2)
    aux2 = cross_product(vect2, vect3)

    cosa = dot_product(aux1,aux2)/(norm_vector(aux1)*norm_vector(aux2))

    if cosa>=1.0:
        cosa=1.0
    if cosa<=-1.0:
        cosa=-1.0

    ang = math.degrees(math.acos(cosa))

    aux3 = cross_product(aux1,aux2)

    if dot_product(aux3,vect2)<=0:
        ang=-ang

    return ang

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

