from depdigest import dep_digest

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest()
@dep_digest("openmm", when={"engine": "OpenMM"})
def get_potential_energy(
    molecular_system,
    selection="all",
    decomposition=False,
    platform="CPU",
    engine="OpenMM",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Calculating the potential energy of a molecular system or selected subsystem.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    decomposition : object, default=False
        Argument decomposition.
    platform : str, default='CPU'
        Execution platform name understood by the selected engine. OpenMM
        examples include 'Reference', 'CPU', 'CUDA' and 'OpenCL'; registered
        plugins are also admitted. Names are case-sensitive in this adapter.
        Selects newly constructed contexts; existing Context/Simulation inputs
        retain their actual platform. Unknown names and known unavailable
        platforms have separate native diagnostics. Device failures propagate.
    engine : str, default='OpenMM'
        Computation engine. Currently only 'OpenMM' is implemented.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity or dict
        Total potential energy in standard units (`kJ/mol`), or dictionary of decomposed energy terms if `decomposition=True`.


    Raises
    ------
    ExecutionPlatformUnavailableError
        If a recognized execution platform is not registered by the engine.
    ArgumentChoiceError
        If a requested platform name is unknown to the selected engine.
    LibraryNotFoundError
        If the selected execution engine is not installed.

    .. versionadded:: 1.0.0
    """

    from molsysmt import convert, get_form, has_attribute
    from molsysmt.configure import default_attribute

    if engine == "OpenMM":
        import openmm as mm

        form_in = get_form(molecular_system)

        if form_in == "openmm.Context":
            if is_all(selection):
                context = molecular_system
            else:
                from molsysmt.form.openmm_Context import extract

                context = extract(molecular_system, selection=selection, syntax=syntax)

        elif form_in == "openmm.Simulation":
            if is_all(selection):
                context = molecular_system.context
            else:
                from molsysmt.form.openmm_Simulation import extract

                context = extract(molecular_system, selection=selection, syntax=syntax)

        else:
            extra_conversion_arguments = {}

            possible_missing_attributes = [
                "forcefield",
                "water_model",
                "implicit_solvent",
                "constraints",
                "non_bonded_method",
                "switch_distance",
                "dispersion_correction",
                "ewald_error_tolerance",
                "integrator",
                "temperature",
                "friction",
                "time_step",
            ]

            for att in possible_missing_attributes:
                if not has_attribute(molecular_system, att):
                    extra_conversion_arguments[att] = default_attribute[att]

            context = convert(
                molecular_system,
                to_form="openmm.Context",
                selection=selection,
                syntax=syntax,
                **extra_conversion_arguments,
                platform=platform,
            )

        if decomposition:
            tmp_system = context.getSystem()

            forcegroups = {}
            for ii in range(tmp_system.getNumForces()):
                force = tmp_system.getForce(ii)
                force.setForceGroup(ii)
                forcegroups[force] = ii

            tmp_context = mm.Context(
                tmp_system, mm.VerletIntegrator(0.001), context.getPlatform()
            )
            tmp_context.setPositions(context.getState(getPositions=True).getPositions())

            context_forcegroups = {}
            for forcegroup, ii in forcegroups.items():
                context_forcegroups[forcegroup.getName()] = tmp_context.getState(
                    getEnergy=True, groups={ii}
                )

            output = {}
            for forcegroup_name, tmp_context in context_forcegroups.items():
                output[forcegroup_name] = tmp_context.getPotentialEnergy()

            for energy_term, energy_value in output.items():
                output[energy_term] = puw.standardize(energy_value)

        else:
            state = context.getState(getEnergy=True)
            output = state.getPotentialEnergy()
            output = puw.standardize(output)

        return output

    else:
        raise NotImplementedError
