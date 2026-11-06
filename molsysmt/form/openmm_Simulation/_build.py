"""Building OpenMM simulations from complete, explicitly supplied inputs."""

from depdigest import dep_digest


@dep_digest("openmm")
def build_simulation(
    topology,
    system,
    coordinates,
    integrator="Langevin",
    temperature="300.0 K",
    collisions_rate="1.0 1/ps",
    integration_timestep="2.0 fs",
    platform="CPU",
):
    """
    Performing build simulation on form openmm.Simulation.


    Parameters
    ----------
    topology : object
        Argument topology.
    system : object
        Argument system.
    coordinates : object
        Argument coordinates.
    integrator : object, default='Langevin'
        Argument integrator.
    temperature : object, default='300.0 K'
        Argument temperature.
    collisions_rate : object, default='1.0 1/ps'
        Argument collisions_rate.
    integration_timestep : object, default='2.0 fs'
        Argument integration_timestep.
    platform : str, default='CPU'
        Exact OpenMM platform name, such as 'Reference', 'CPU', 'CUDA' or
        'OpenCL', or another registered plugin name. An unknown name is
        rejected; a known unregistered platform has an availability diagnostic.
        Device/context initialization failures are retained as engine errors.
        No different platform is selected on failure.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    if coordinates is None:
        from molsysmt._private.smonitor import NotCompatibleConversionError

        raise NotCompatibleConversionError(
            "openmm.Topology",
            "openmm.Simulation",
            {"coordinates"},
            caller="molsysmt.form.openmm_Simulation._build.build_simulation",
        )

    import openmm as mm
    from openmm.app import Simulation

    from molsysmt import pyunitwizard as puw

    if integrator != "Langevin":
        from molsysmt._private.smonitor import ArgumentError

        raise ArgumentError(
            "integrator",
            value=integrator,
            caller="molsysmt.form.openmm_Simulation._build.build_simulation",
        )

    temperature = puw.convert(temperature, to_unit="K", to_form="openmm.unit")
    collisions_rate = puw.convert(
        collisions_rate,
        to_unit="1/ps",
        to_form="openmm.unit",
    )
    integration_timestep = puw.convert(
        integration_timestep,
        to_unit="fs",
        to_form="openmm.unit",
    )
    openmm_integrator = mm.LangevinIntegrator(
        temperature,
        collisions_rate,
        integration_timestep,
    )

    openmm_platform = None
    if platform is not None:
        from molsysmt.third_party.openmm.platforms._resolve import resolve_platform

        openmm_platform = resolve_platform(
            platform, "molsysmt.form.openmm_Simulation._build.build_simulation"
        )

    simulation = Simulation(
        topology,
        system,
        openmm_integrator,
        platform=openmm_platform,
    )

    if getattr(coordinates, "ndim", None) == 3:
        coordinates = coordinates[0]
    coordinates = puw.convert(
        coordinates,
        to_unit="nm",
        to_form="openmm.unit",
    )
    simulation.context.setPositions(coordinates)

    return simulation
