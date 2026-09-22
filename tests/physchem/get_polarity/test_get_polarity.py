""" """

# Import package, test suite, and other packages as needed

import molsysmt as msm

# Distance between atoms in space and time


def test_get_polarity_1():

    molsys = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.h5msm"],
        selection='molecule_type=="protein"',
    )

    n_groups = msm.get(molsys, element="system", n_groups=True)
    grantham = msm.physchem.get_polarity(molsys, definition="grantham")
    zimmerman = msm.physchem.get_polarity(molsys, definition="zimmerman")

    assert len(grantham) == n_groups
    assert len(zimmerman) == n_groups
