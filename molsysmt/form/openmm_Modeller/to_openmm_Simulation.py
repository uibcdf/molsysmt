from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest


@arg_digest(form="openmm.Modeller")
@dep_digest("openmm")
def to_openmm_Simulation(
    item,
    atom_indices="all",
    structure_indices="all",
    forcefield="AMBER14",
    water_model=None,
    implicit_solvent=None,
    non_bonded_method="no cutoff",
    constraints="hbonds",
    switch_distance=None,
    dispersion_correction=False,
    ewald_error_tolerance=0.0005,
    integrator="Langevin",
    temperature="300.0 K",
    collisions_rate="1.0 1/ps",
    integration_timestep="2.0 fs",
    platform="CPU",
    skip_digestion=False,
):
    """
    Converting from openmm.Modeller to openmm.Simulation.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    forcefield : str, default='AMBER14'
        Force field parameter identifier or name.
    water_model : str, default=None
        Water model parameter identifier (e.g., 'TIP3P').
    implicit_solvent : str, default=None
        Implicit solvent model name if applicable.
    non_bonded_method : object, default='no cutoff'
        Argument non_bonded_method.
    constraints : object, default='hbonds'
        Argument constraints.
    switch_distance : object, default=None
        Argument switch_distance.
    dispersion_correction : object, default=False
        Argument dispersion_correction.
    ewald_error_tolerance : object, default=0.0005
        Argument ewald_error_tolerance.
    integrator : object, default='Langevin'
        Argument integrator.
    temperature : object, default='300.0 K'
        Argument temperature.
    collisions_rate : object, default='1.0 1/ps'
        Argument collisions_rate.
    integration_timestep : object, default='2.0 fs'
        Argument integration_timestep.
    platform : str, default='CPU'
        OpenMM platform name ('Reference', 'CPU', 'CUDA', 'OpenCL').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Simulation
        Resulting object in openmm.Simulation form.


    .. versionadded:: 1.0.0
    """

    from .to_openmm_Topology import to_openmm_Topology
    from . import get_coordinates_from_atom
    from molsysmt.form.openmm_Topology.to_openmm_Simulation import (
        to_openmm_Simulation as openmm_Topology_to_openmm_Simulation,
    )

    topology = to_openmm_Topology(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    coordinates = get_coordinates_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    return openmm_Topology_to_openmm_Simulation(
        topology,
        coordinates=coordinates,
        forcefield=forcefield,
        water_model=water_model,
        implicit_solvent=implicit_solvent,
        non_bonded_method=non_bonded_method,
        constraints=constraints,
        switch_distance=switch_distance,
        dispersion_correction=dispersion_correction,
        ewald_error_tolerance=ewald_error_tolerance,
        integrator=integrator,
        temperature=temperature,
        collisions_rate=collisions_rate,
        integration_timestep=integration_timestep,
        platform=platform,
        skip_digestion=True,
    )
