from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest


@arg_digest(form="molsysmt.MolSys")
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
    Converting from molsysmt.MolSys to openmm.Simulation.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
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
    from . import get_coordinates_from_atom
    from molsysmt._private.variables import is_all
    from molsysmt.form.openmm_Topology.to_openmm_Simulation import (
        to_openmm_Simulation as openmm_Topology_to_openmm_Simulation,
    )

    if is_all(structure_indices):
        topology_structure_indices = [0]
    else:
        try:
            topology_structure_indices = [structure_indices[0]]
        except TypeError:
            topology_structure_indices = [structure_indices]

    topology = to_openmm_Topology(
        item,
        atom_indices=atom_indices,
        structure_indices=topology_structure_indices,
        skip_digestion=True,
    )
    coordinates = get_coordinates_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    if coordinates is None:
        from molsysmt._private.smonitor import NotCompatibleConversionError

        raise NotCompatibleConversionError(
            "molsysmt.MolSys",
            "openmm.Simulation",
            {"coordinates"},
            caller="molsysmt.form.molsysmt_MolSys.to_openmm_Simulation",
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
