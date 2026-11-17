""" """

# Import package, test suite, and other packages as needed

import numpy as np
import pytest

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


def _two_particles(mm):
    system = mm.System()
    for _ in range(2):
        system.addParticle(12)
    system.setDefaultPeriodicBoxVectors(
        mm.Vec3(6, 0, 0), mm.Vec3(0, 6, 0), mm.Vec3(0, 0, 6)
    )
    return system


def _custom_bond(mm, expression, name, group, *, periodic=False):
    force = mm.CustomBondForce(expression)
    force.setName(name)
    force.setForceGroup(group)
    force.setUsesPeriodicBoundaryConditions(periodic)
    return force


def _context(mm, system, separation):
    context = mm.Context(
        system,
        mm.VerletIntegrator(0.001),
        mm.Platform.getPlatformByName("CPU"),
        {"Threads": "1"},
    )
    context.setPositions([[0, 0, 0], [separation, 0, 0]] * mm.unit.nanometer)
    return context


def test_decomposition_preserves_duplicate_terms_and_original_force_groups():
    import molsysmt as msm

    mm = pytest.importorskip("openmm")
    system = _two_particles(mm)
    for energy, group, name in [
        (2, 6, "bond"),
        (5, 9, "bond"),
        (11, 12, "bond [force 0]"),
    ]:
        force = _custom_bond(mm, str(energy), name, group)
        force.addBond(0, 1, [])
        system.addForce(force)
    context = _context(mm, system, 0.25)
    for _ in range(2):
        with puw.context(standard_units=["kcal/mol"]):
            terms = msm.molecular_mechanics.get_potential_energy(
                context, decomposition=True
            )
            assert list(terms) == [
                "bond [force 0] [force 0]",
                "bond [force 1]",
                "bond [force 0]",
            ]
            assert all(
                puw.get_unit(value) == puw.unit("kcal/mol") for value in terms.values()
            )
            assert [
                puw.get_value(value, to_unit="kJ/mol") for value in terms.values()
            ] == pytest.approx([2, 5, 11])
        assert [force.getForceGroup() for force in system.getForces()] == [6, 9, 12]
        assert puw.get_value(
            msm.molecular_mechanics.get_potential_energy(context), to_unit="kJ/mol"
        ) == pytest.approx(18)


def test_decomposition_uses_live_box_and_active_global_and_bond_parameters():
    import molsysmt as msm

    mm = pytest.importorskip("openmm")
    system = _two_particles(mm)
    force = _custom_bond(mm, "k*r+c", "periodic", 3, periodic=True)
    force.addGlobalParameter("k", 2)
    force.addPerBondParameter("c")
    force.addBond(0, 1, [1])
    system.addForce(force)
    context = _context(mm, system, 2.6)
    context.setParameter("k", 9)
    context.setPeriodicBoxVectors(mm.Vec3(4, 0, 0), mm.Vec3(0, 4, 0), mm.Vec3(0, 0, 4))
    force.setBondParameters(0, 0, 1, [3])
    force.updateParametersInContext(context)
    force.setBondParameters(0, 0, 1, [20])
    state = context.getState(getPositions=True)

    terms = msm.molecular_mechanics.get_potential_energy(context, decomposition=True)
    assert list(terms) == ["periodic"]
    assert puw.get_value(terms["periodic"], to_unit="kJ/mol") == pytest.approx(15.6)
    assert context.getParameter("k") == 9
    assert force.getForceGroup() == 3
    assert list(force.getBondParameters(0)[2]) == [20]
    after = context.getState(getPositions=True)
    for old, new in [
        (state.getPositions(asNumpy=True), after.getPositions(asNumpy=True)),
        (
            state.getPeriodicBoxVectors(asNumpy=True),
            after.getPeriodicBoxVectors(asNumpy=True),
        ),
    ]:
        np.testing.assert_array_equal(
            old.value_in_unit(mm.unit.nanometer), new.value_in_unit(mm.unit.nanometer)
        )


@pytest.mark.parametrize("shared", [False, True])
def test_simulation_decomposition_uses_reciprocal_group_and_refuses_overlap(shared):
    import molsysmt as msm
    from molsysmt._private.smonitor import NotImplementedMethodError

    mm = pytest.importorskip("openmm")
    from openmm import app

    system = _two_particles(mm)
    nonbonded = mm.NonbondedForce()
    nonbonded.setNonbondedMethod(nonbonded.Ewald)
    nonbonded.setCutoffDistance(1.0)
    nonbonded.setForceGroup(0)
    nonbonded.setReciprocalSpaceForceGroup(7)
    for charge in (-1, 1):
        nonbonded.addParticle(charge, 0.1, 0)
    system.addForce(nonbonded)
    group = 7 if shared else 4
    bond = _custom_bond(mm, "3", "bond", group)
    bond.addBond(0, 1, [])
    system.addForce(bond)

    topology = app.Topology()
    residue = topology.addResidue("LIG", topology.addChain())
    for name in ("C1", "C2"):
        topology.addAtom(name, app.element.carbon, residue)
    simulation = app.Simulation(
        topology,
        system,
        mm.VerletIntegrator(0.001),
        mm.Platform.getPlatformByName("CPU"),
        {"Threads": "1"},
    )
    context = simulation.context
    context.setPositions([[0, 0, 0], [0.5, 0, 0]] * mm.unit.nanometer)
    total = context.getState(getEnergy=True).getPotentialEnergy()
    if shared:
        with pytest.raises(NotImplementedMethodError, match="overlapping force groups"):
            msm.molecular_mechanics.get_potential_energy(simulation, decomposition=True)
    else:
        terms = msm.molecular_mechanics.get_potential_energy(
            simulation, decomposition=True
        )
        assert list(terms) == ["NonbondedForce", "bond"]
        assert puw.get_value(terms["bond"], to_unit="kJ/mol") == pytest.approx(3)
        total_value = total.value_in_unit(mm.unit.kilojoule_per_mole)
        assert puw.get_value(
            terms["NonbondedForce"], to_unit="kJ/mol"
        ) == pytest.approx(total_value - 3)
    assert nonbonded.getForceGroup() == 0
    assert nonbonded.getReciprocalSpaceForceGroup() == 7
    assert bond.getForceGroup() == group
    assert context.getState(getEnergy=True).getPotentialEnergy() == total


def test_decomposition_refuses_a_context_with_unassigned_live_energy():
    import molsysmt as msm
    from molsysmt._private.smonitor import StructuralInconsistencyError

    mm = pytest.importorskip("openmm")
    system = _two_particles(mm)
    force = _custom_bond(mm, "2", "bond", 6)
    force.addBond(0, 1, [])
    system.addForce(force)
    context = _context(mm, system, 0.25)
    force.setForceGroup(5)
    with pytest.raises(StructuralInconsistencyError, match="do not reproduce"):
        msm.molecular_mechanics.get_potential_energy(context, decomposition=True)
    assert force.getForceGroup() == 5
    assert puw.get_value(
        msm.molecular_mechanics.get_potential_energy(context), to_unit="kJ/mol"
    ) == pytest.approx(2)
