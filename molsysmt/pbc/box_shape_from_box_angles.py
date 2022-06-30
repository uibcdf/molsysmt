from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np
from molsysmt import puw

def box_shape_from_box_angles(angles, check=True):

    shape = None

    if angles is not None:

        alpha = angles[:,0].mean()
        beta = angles[:,1].mean()
        gamma = angles[:,2].mean()

        alpha = puw.get_value(alpha, to_unit='degrees')
        beta = puw.get_value(beta, to_unit='degrees')
        gamma = puw.get_value(gamma, to_unit='degrees')

        if np.allclose([alpha, beta, gamma], [90.0, 90.0, 90.0]):
            shape = 'cubic'
        elif np.allclose([alpha, beta, gamma], [70.52878, 109.471221, 70.52878]):
            shape = 'truncated octahedral'
        elif np.allclose([alpha, beta, gamma], [60.0, 60.0, 90.0]):
            shape = 'rhombic dodecahedral'
        else:
            shape = 'triclinic'

    return shape

