from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.System")
@dep_digest("openmm")
def to_openmm_Context(
    item,
    atom_indices="all",
    coordinates=None,
    integrator="Langevin",
    temperature="300 kelvin",
    friction="1.0/picoseconds",
    time_step="2 femtoseconds",
    platform="CUDA",
    skip_digestion=False,
):
    """
    Converting from openmm.System to openmm.Context.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : object, default=None
        Argument coordinates.
    integrator : object, default='Langevin'
        Argument integrator.
    temperature : object, default='300 kelvin'
        Argument temperature.
    friction : object, default='1.0/picoseconds'
        Argument friction.
    time_step : object, default='2 femtoseconds'
        Argument time_step.
    platform : str, default='CUDA'
        Exact OpenMM platform name, such as 'Reference', 'CPU', 'CUDA' or
        'OpenCL', or another registered plugin name. An unknown name is
        rejected; a known unregistered platform has an availability diagnostic.
        Device/context initialization failures are retained as engine errors.
        No different platform is selected on failure.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Context
        Resulting object in openmm.Context form.


    .. versionadded:: 1.0.0
    """

    import openmm as mm

    from molsysmt import pyunitwizard as puw
    from molsysmt.form.openmm_Context import set_coordinates_to_atom

    temperature = puw.convert(temperature, to_form="openmm.unit")
    friction = puw.convert(friction, to_form="openmm.unit")
    time_step = puw.convert(time_step, to_form="openmm.unit")

    if integrator == "Langevin":
        integrator = mm.LangevinIntegrator(temperature, friction, time_step)

    from molsysmt.third_party.openmm.platforms._resolve import resolve_platform

    platform = resolve_platform(
        platform, "molsysmt.form.openmm_System.to_openmm_Context"
    )

    context = mm.Context(item, integrator, platform)

    if coordinates is not None:
        set_coordinates_to_atom(
            context, indices=atom_indices, value=coordinates, skip_digestion=True
        )

    return context
