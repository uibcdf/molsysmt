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
    """Building an OpenMM Simulation without inventing an initial structure."""

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
        openmm_platform = (
            mm.Platform.getPlatformByName(platform)
            if isinstance(platform, str)
            else platform
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
