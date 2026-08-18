from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest


@arg_digest(form="openmm.Topology")
@dep_digest("openmm")
def to_openmm_Simulation(
    item,
    atom_indices="all",
    coordinates=None,
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
    Converting from openmm.Topology to openmm.Simulation.

    Parameters
    ----------
    item : openmm.Topology
        Source item in openmm.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    forcefield : object
        Argument forcefield.
    water_model : object
        Argument water_model.
    implicit_solvent : object
        Argument implicit_solvent.
    non_bonded_method : object
        Argument non_bonded_method.
    constraints : object
        Argument constraints.
    switch_distance : object
        Argument switch_distance.
    dispersion_correction : object
        Argument dispersion_correction.
    ewald_error_tolerance : object
        Argument ewald_error_tolerance.
    integrator : object
        Argument integrator.
    temperature : object
        Argument temperature.
    collisions_rate : object
        Argument collisions_rate.
    integration_timestep : object
        Argument integration_timestep.
    platform : object
        Argument platform.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Simulation
        Resulting object in openmm.Simulation form.

    .. versionadded:: 1.0.0
    """

    from .to_openmm_Topology import to_openmm_Topology
    from .to_openmm_System import to_openmm_System
    from molsysmt.form.openmm_Simulation._build import build_simulation

    topology = to_openmm_Topology(
        item,
        atom_indices=atom_indices,
        copy_if_all=False,
        skip_digestion=True,
    )
    system = to_openmm_System(
        topology,
        forcefield=forcefield,
        water_model=water_model,
        implicit_solvent=implicit_solvent,
        non_bonded_method=non_bonded_method,
        constraints=constraints,
        switch_distance=switch_distance,
        dispersion_correction=dispersion_correction,
        ewald_error_tolerance=ewald_error_tolerance,
        skip_digestion=True,
    )
    return build_simulation(
        topology,
        system,
        coordinates,
        integrator=integrator,
        temperature=temperature,
        collisions_rate=collisions_rate,
        integration_timestep=integration_timestep,
        platform=platform,
    )
