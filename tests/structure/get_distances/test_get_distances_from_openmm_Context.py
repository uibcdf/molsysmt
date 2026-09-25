"""
Unit and regression test for the get_distances function over an openmm.Context object in molsysmt.
"""

# Import package, test suite, and other packages as needed
from importlib.util import find_spec

import pytest

if find_spec("openmm") is None:
    pytest.skip("OpenMM is an optional backend", allow_module_level=True)

from openmm import app  # noqa: E402

topology = app.Topology()
chain = topology.addChain("A")
residue = topology.addResidue("Ar", chain)
atom = topology.addAtom(name="Ar", element=app.element.argon, residue=residue)
chain = topology.addChain("B")
residue = topology.addResidue("Ar", chain)
atom = topology.addAtom(name="Ar", element=app.element.argon, residue=residue)

# def test_get_distances_from_openmm_Context_1():
#
#    system = mm.System()
#    system.addParticle(atom.element.mass) # masa del átomo de argón
#    system.addParticle(atom.element.mass) # masa del átomo de argón
#
#    temperature = 300*unit.kelvin
#    integration_timestep = 2.0*unit.femtoseconds
#    saving_interval = 1.00*unit.picoseconds
#    logging_interval = 100.00*unit.picoseconds
#    simulation_time = 1000.*unit.picoseconds
#
#    saving_steps = int(saving_interval/integration_timestep)
#    logging_steps = int(logging_interval/integration_timestep)
#    md_steps = int(simulation_time/integration_timestep)
#    friction   = 5.0/unit.picoseconds
#    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
#    platform = mm.Platform.getPlatformByName('CPU')
#    context = mm.Context(system, integrator, platform)
#    initial_positions  = [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]] * unit.nanometers
#    context.setPositions(initial_positions)
#    Lbox = 2.0
#    v1 = [Lbox,0,0] * unit.nanometers
#    v2 = [0,Lbox,0] * unit.nanometers
#    v3 = [0,0,Lbox] * unit.nanometers
#    context.setPeriodicBoxVectors(v1, v2, v3)
#
#
#    assert
