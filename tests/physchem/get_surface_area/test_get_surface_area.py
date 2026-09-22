""" """

# Import package, test suite, and other packages as needed

import molsysmt as msm

# Distance between atoms in space and time


def test_get_surface_area_1():

    molsys = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.h5msm"],
        selection='molecule_type=="protein"',
    )

    n_groups = msm.get(molsys, element="system", n_groups=True)
    grantham = msm.physchem.get_surface_area(molsys, definition="collantes")

    assert len(grantham) == n_groups
