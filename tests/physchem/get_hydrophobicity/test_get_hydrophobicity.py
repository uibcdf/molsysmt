""" """

# Import package, test suite, and other packages as needed

import molsysmt as msm

# Distance between atoms in space and time


def test_get_hydrophobicity_1():

    molsys = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.h5msm"],
        selection='molecule_type=="protein"',
    )

    n_groups = msm.get(molsys, element="system", n_groups=True)
    for definition in (
        "eisenberg",
        "rao",
        "sweet",
        "kyte",
        "abraham",
        "bull",
        "guy",
        "miyazawa",
        "roseman",
        "wolfenden",
        "chothia",
        "hopp",
        "manavalan",
        "black",
        "fauchere",
    ):
        values = msm.physchem.get_hydrophobicity(molsys, definition=definition)
        assert len(values) == n_groups
