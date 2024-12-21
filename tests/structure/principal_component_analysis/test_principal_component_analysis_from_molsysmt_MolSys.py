"""
Unit and regression test for the get_contacts module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

# Distance between atoms in space and time

def test_principal_component_analysis_from_molsysmt_MolSys_1():

    molecular_system = msm.systems['pentalanine']['traj_pentalanine.h5']
    molecular_system = msm.convert(molecular_system, to_form='molsysmt.MolSys')

    pcs, sigmas = msm.structure.principal_component_analysis(molecular_system, selection='atom_name=="CA"')

    good_pc0 = np.array([-0.31318154, -0.27878168, -0.23782996, -0.19504104, -0.14894687,
                         -0.31654838, -0.35124151, -0.37907152, -0.40324586, -0.42133246,
                         -0.00120831, -0.0019539 , -0.00200411, -0.00092844,  0.00131092])

    good_sigmas = np.array([-7.61673223e+00, -2.40353497e+00, -7.07258185e-01, -5.66336274e-01,
                            -4.55056633e-01, -7.10380242e-03, -3.47446577e-03,  1.28211399e-03,
                             1.99369789e-03,  4.33715991e-03,  3.91734124e-02,  4.61545377e-01,
                             4.96569155e-01,  8.32111142e-01,  9.15973936e-01]) 

    assert np.allclose(pcs[0], good_pc0)
    assert np.allclose(sigmas, good_sigmas)
