import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt import systems


openmm = pytest.importorskip("openmm")


@pytest.fixture(scope="module")
def alanine_dipeptide():
    return msm.convert(
        systems["alanine dipeptide"]["alanine_dipeptide.h5msm"],
        to_form="molsysmt.MolSys",
    )


@pytest.fixture(scope="module")
def trp_cage():
    return msm.convert(
        systems["Trp-Cage"]["1l2y.pdb"],
        to_form="molsysmt.MolSys",
    )


def _context_positions(simulation):
    positions = simulation.context.getState(getPositions=True).getPositions(
        asNumpy=True
    )
    return puw.get_value(positions, to_unit="nm")


def test_molsys_builds_a_cpu_simulation_by_default(alanine_dipeptide):
    simulation = msm.convert(
        alanine_dipeptide,
        to_form="openmm.Simulation",
    )

    assert isinstance(simulation, openmm.app.Simulation)
    assert simulation.context.getPlatform().getName() == "CPU"
    assert simulation.topology.getNumAtoms() == 22
    assert simulation.system.getNumParticles() == 22
    assert np.allclose(
        _context_positions(simulation),
        puw.get_value(
            alanine_dipeptide.structures.coordinates[0],
            to_unit="nm",
        ),
    )


def test_requested_structure_order_selects_the_initial_state(trp_cage):
    simulation = msm.convert(
        trp_cage,
        to_form="openmm.Simulation",
        structure_indices=[19, 0],
        platform="CPU",
    )

    assert np.allclose(
        _context_positions(simulation),
        puw.get_value(trp_cage.structures.coordinates[19], to_unit="nm"),
    )


def test_all_structures_uses_the_first_box_and_initial_state(trp_cage):
    simulation = msm.convert(trp_cage, to_form="openmm.Simulation")

    assert np.allclose(
        _context_positions(simulation),
        puw.get_value(trp_cage.structures.coordinates[0], to_unit="nm"),
    )
    assert np.allclose(
        puw.get_value(simulation.topology.getPeriodicBoxVectors(), to_unit="nm"),
        puw.get_value(trp_cage.structures.box[0], to_unit="nm"),
    )


def test_molsys_without_coordinates_is_rejected(alanine_dipeptide):
    source = alanine_dipeptide.copy()
    source.structures.coordinates = None

    with pytest.raises(msm.NotCompatibleConversionError, match="coordinates"):
        msm.convert(source, to_form="openmm.Simulation")


def test_openmm_topology_requires_explicit_coordinates(alanine_dipeptide):
    topology = msm.convert(alanine_dipeptide, to_form="openmm.Topology")

    with pytest.raises(msm.NotCompatibleConversionError, match="coordinates"):
        msm.convert(topology, to_form="openmm.Simulation")

    simulation = msm.convert(
        topology,
        to_form="openmm.Simulation",
        coordinates=alanine_dipeptide.structures.coordinates[[0]],
        platform="CPU",
    )
    assert np.allclose(
        _context_positions(simulation),
        puw.get_value(
            alanine_dipeptide.structures.coordinates[0],
            to_unit="nm",
        ),
    )


def test_pdb_and_modeller_routes_build_usable_simulations():
    pdb_file = systems["Trp-Cage"]["1l2y.pdb"]
    modeller = msm.convert(
        pdb_file,
        to_form="openmm.Modeller",
        structure_indices=0,
    )

    from_pdb = msm.convert(
        pdb_file,
        to_form="openmm.Simulation",
        structure_indices=0,
        platform="CPU",
    )
    from_modeller = msm.convert(
        modeller,
        to_form="openmm.Simulation",
        platform="CPU",
    )

    assert from_pdb.system.getNumParticles() == 304
    assert from_modeller.system.getNumParticles() == 304
    assert np.allclose(
        _context_positions(from_pdb),
        _context_positions(from_modeller),
    )


def test_system_alone_does_not_advertise_simulation_construction():
    table = msm.supported.conversions(
        from_form="openmm.System",
        to_form="openmm.Simulation",
    )

    assert not bool(table.data.iloc[0, 0])
