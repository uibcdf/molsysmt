"""
Unit and regression test for the get_structure_alignment module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_align_principal_axes_molsysmt_MolSys_1():

    crd = msm.systems['POPC']['popc.crd']
    psf = msm.systems['POPC']['popc.psf']
    molsys = msm.convert([crd, psf])

    axes_1, momenta_1 = msm.structure.get_principal_axes(molsys)

    good_axes_1 = np.array([[[ 0.09213962, -0.02624376, -0.9954002 ],
                             [ 0.56239734,  0.82631277,  0.03027277],
                             [-0.82171742,  0.56259975, -0.09089556]]])

    molsys_2 = msm.structure.align_principal_axes(molsys, axes=[[1,0,0],[0,1,0],[0,0,1]])

    axes_2, momenta_2 = msm.structure.get_principal_axes(molsys_2)

    good_axes_2 = np.array([[[ 1.00000000e+00,  2.87221485e-16,  8.58936055e-17],
                             [-2.87221485e-16,  1.00000000e+00, -3.60822483e-15],
                             [-8.58936055e-17,  3.60822483e-15,  1.00000000e+00]]])

    for ii in range(3):
        if np.sign(axes_1[0,ii,0]) != np.sign(good_axes_1[0,ii,0]):
            good_axes_1[0,ii,:] = -good_axes_1[0,ii,:]
        if np.sign(axes_2[0,ii,0]) != np.sign(good_axes_2[0,ii,0]):
            good_axes_2[0,ii,:] = -good_axes_2[0,ii,:]

    assert np.allclose(momenta_1, momenta_2), f"{momenta_1} {momenta_2}"
    assert np.allclose(axes_1, good_axes_1), f"{axes_1} {good_axes_1}"
    assert np.allclose(axes_2, good_axes_2), f"{axes_2} {good_axes_2}"


