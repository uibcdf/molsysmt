import numpy as np
import numba as nb

@nb.jit(void(nb.float64[:], nb.float64[:,:], nb.float64[:,:], nb.boolean), nopython=True)
def pbc(vector, box, inv, ortho):

    if ortho:

        vector[0]=vector[0]-box[0,0]*round(vector[0]/box[0,0])
        vector[1]=vector[1]-box[1,1]*round(vector[1]/box[1,1])
        vector[2]=vector[2]-box[2,2]*round(vector[2]/box[2,2])

    else:

        vaux[0]=inv[0,0]*vector[0]+inv[1,0]*vector[1]+inv[2,0]*vector[2]
        vaux[1]=                   inv[1,1]*vector[1]+inv[2,1]*vector[2]
        vaux[2]=                                      inv[2,2]*vector[2]
        vaux[0]=vauxr[0]-round(vaux[0])
        vaux[1]=vauxr[1]-round(vaux[1])
        vaux[2]=vauxr[2]-round(vaux[2])
        vector[0]=box[0,0]*vaux[0]+box[1,0]*vaux[1]+box[2,0]*vaux[2]
        vector[1]=                 box[1,1]*vaux[1]+box[2,1]*vaux[2]
        vector[2]=                                  box[2,2]*vaux[2]

    pass

@nb.jit(void(nb.float64[:], nb.float64[:,:], nb.float64[:,:], nb.boolean), nopython=True)
def mic(vector, box, inv, ortho):

    pbc(vector, box, inv, ortho)

    if not ortho:

        vmin=vector
        dmin=(vmin[0]*vmin[0]+vmin[1]*vmin[1]+vmin[2]*vmin[2])

        for ii in [-1,0,1]:
            vaux=vector+ii*box[0,:]
            for jj in [-1,0,1]:
                vaux2=vaux+jj*box[1,:]
                for kk in [-1,0,1]:
                    vaux3[:]=vaux2[:]+kk*box[2,:]
                    d=(vaux3[0]*vaux3[0]+vaux3[1]*vaux3[1]+vaux3[2]*vaux3[2])
                    if dmin>d:
                        vmin=vaux3
                        dmin=d

        vector=vmin

    pass
