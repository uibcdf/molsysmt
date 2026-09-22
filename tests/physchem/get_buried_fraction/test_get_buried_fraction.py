""" """

# Import package, test suite, and other packages as needed

import molsysmt as msm


def test_get_buried_fraction_1():

    molsys = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.h5msm"],
        selection='molecule_type=="protein"',
    )

    n_groups = msm.get(molsys, element="system", n_groups=True)
    janin = msm.physchem.get_buried_fraction(molsys, definition="janin")

    assert len(janin) == n_groups
