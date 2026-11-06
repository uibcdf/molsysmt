"""Checking potential forces against a literal harmonic-bond derivative."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures

openmm = pytest.importorskip("openmm")


@pytest.mark.parametrize("magnitude", [False, True])
@pytest.mark.parametrize("source_kind", ["context", "native_structures_and_system"])
def test_harmonic_forces_follow_the_literal_negative_energy_gradient(
    source_kind, magnitude
):
    # U(r) = 1/2 k(r-r0)^2; at r=0.2 nm, k=100 kJ/(mol nm^2), r0=0.1 nm,
    # the first atom feels +10 and the second -10 kJ/(mol nm) along x.
    system = openmm.System()
    system.addParticle(12.0)
    system.addParticle(12.0)
    bond = openmm.HarmonicBondForce()
    bond.addBond(0, 1, 0.1, 100.0)
    system.addForce(bond)
    xyz = np.array([[[0.0, 0.0, 0.0], [0.2, 0.0, 0.0]]])
    if source_kind == "context":
        source = openmm.Context(
            system,
            openmm.VerletIntegrator(0.001),
            openmm.Platform.getPlatformByName("Reference"),
        )
        source.setPositions(xyz[0] * openmm.unit.nanometer)
    else:
        structures = Structures()
        structures.coordinates = puw.quantity(xyz, "nm")
        source = [structures, system]
    result = msm.molecular_mechanics.get_forces(
        source,
        selection=[1, 0, 1],
        structure_indices=[0],
        magnitude=magnitude,
        platform="Reference",
    )
    expected = np.array([[[-10.0, 0.0, 0.0], [10.0, 0.0, 0.0], [-10.0, 0.0, 0.0]]])
    if magnitude:
        expected = np.linalg.norm(expected, axis=-1)
    assert result.shape == expected.shape
    assert puw.get_unit(result) == puw.unit("kJ/(mol*nm)")
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="kJ/(mol*nm)"), expected, atol=1e-12, rtol=0
    )
