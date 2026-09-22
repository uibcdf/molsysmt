""" """

# Import package, test suite, and other packages as needed

from molsysmt import pyunitwizard as puw


def test_get_potential_energy_1():

    import molsysmt as msm

    molecular_system = msm.convert(
        msm.systems["Barnase-Barstar"]["barnase_barstar.h5msm"]
    )

    U = msm.molecular_mechanics.get_potential_energy(molecular_system)

    assert puw.get_unit(U) == puw.unit("kilojoule/mole")


def test_get_potential_energy_2():

    import molsysmt as msm

    molecular_system = msm.convert(
        msm.systems["Barnase-Barstar"]["barnase_barstar.h5msm"]
    )

    U_dict = msm.molecular_mechanics.get_potential_energy(
        molecular_system, selection='molecule_name=="BARSTAR"', decomposition=True
    )

    assert list(U_dict.keys()) == [
        "HarmonicBondForce",
        "NonbondedForce",
        "PeriodicTorsionForce",
        "CMMotionRemover",
        "HarmonicAngleForce",
    ]
