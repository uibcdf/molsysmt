""" """

# Import package, test suite, and other packages as needed

import molsysmt as msm


def test_get_transmembrane_tendency_1():

    molsys = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.h5msm"],
        selection='molecule_type=="protein"',
    )

    n_groups = msm.get(molsys, element="system", n_groups=True)
    zhao = msm.physchem.get_transmembrane_tendency(molsys, definition="zhao")
    senes = msm.physchem.get_transmembrane_tendency(molsys, definition="senes")

    assert len(zhao) == n_groups
    assert len(senes) == n_groups
