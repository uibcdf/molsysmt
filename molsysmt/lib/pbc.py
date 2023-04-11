import numpy as np

@nb.jit(void(nb.float64[:], nb.float64[:,:], nb.float64[:,:], nb.boolean), nopython=True)
def pbc(vector, box, inv, ortho):

    if ortho:
        vector[0]=vector[0]-box[0,0]*round(vector[0]/box[0,0])
        vector[1]=vector[1]-box[1,1]*round(vector[1]/box[1,1])
        vector[2]=vector[2]-box[2,2]*round(vector[2]/box[2,2])
    else:

        vaux[0]=inv[0,0]*vector[0]+inv[1,0]*vector[1]+inv[2,0]*vector[2]
        vaux[1]=                   inv[1,1]*vector[1]+inv[2,1]*vector[2]
    vaux(3)=                                      inv(3,3)*vector(3)
    vaux(1)=vaux(1)-NINT(vaux(1))*1.0
    vaux(2)=vaux(2)-NINT(vaux(2))*1.0
    vaux(3)=vaux(3)-NINT(vaux(3))*1.0
    vector(1)=box(1,1)*vaux(1)+box(2,1)*vaux(2)+box(3,1)*vaux(3)
    vector(2)=                 box(2,2)*vaux(2)+box(3,2)*vaux(3)
    vector(3)=                                  box(3,3)*vaux(3)

    vaux(1)=inv(1,1)*vector(1)+inv(2,1)*vector(2)+inv(3,1)*vector(3)
    vaux(2)=                   inv(2,2)*vector(2)+inv(3,2)*vector(3)
    vaux(3)=                                      inv(3,3)*vector(3)
    vaux(1)=vaux(1)-NINT(vaux(1))*1.0
    vaux(2)=vaux(2)-NINT(vaux(2))*1.0
    vaux(3)=vaux(3)-NINT(vaux(3))*1.0
    vector(1)=box(1,1)*vaux(1)+box(2,1)*vaux(2)+box(3,1)*vaux(3)
    vector(2)=                 box(2,2)*vaux(2)+box(3,2)*vaux(3)
    vector(3)=                                  box(3,3)*vaux(3)

    pass

def mic(vector, box, inv, ortho):

    raise NotImplementedError()

