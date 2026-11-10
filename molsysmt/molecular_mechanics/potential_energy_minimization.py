from depdigest import dep_digest

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest


@arg_digest()
@dep_digest("openmm", when={"engine": "OpenMM"})
def potential_energy_minimization(
    molecular_system,
    method="L-BFGS",
    platform="CPU",
    engine="OpenMM",
    to_form=None,
    in_place=False,
    verbose=False,
):
    """
    Minimizing potential energy with the selected engine's local optimizer.

    Performs energy minimization using the chosen backend optimizer. The minimized
    coordinates are applied either in-place to the original molecular system or to
    an independent result for forms supporting the requested copy/conversion.
    Native MolSys examples below make that ownership choice explicit.


    Newly constructed models reject stored controls that the selected adapter
    cannot apply. Inspect the supported physical recipe with
    :func:`molsysmt.molecular_mechanics.get_model_recipe`. A supplied parameterized
    engine model remains authoritative; its construction history is not inferred.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    method : str, default='L-BFGS'
        Local minimization algorithm. OpenMM's ``LocalEnergyMinimizer`` implements
        L-BFGS, so 'L-BFGS' is the only accepted value; any other name is refused.
    platform : str, default='CPU'
        Execution platform name understood by the selected engine. OpenMM
        examples include 'Reference', 'CPU', 'CUDA' and 'OpenCL'; registered
        plugins are also admitted. Selects newly constructed contexts;
        existing Context/Simulation inputs keep their actual platform.
        Unknown names, absent registration and device failures stay distinct.
    engine : str, default='OpenMM'
        Engine performing the minimization. Only 'OpenMM' is implemented.
    to_form : str, default=None
        Form of the returned molecular system when ``in_place=False``. With None the
        input form is preserved.
    in_place : bool, default=False
        Whether the minimized coordinates are written into ``molecular_system``
        instead of being returned in a new molecular system.
    verbose : bool, default=False
        Whether the potential energy before and after the minimization is printed.

    Returns
    -------
    molecular system or None
        When ``in_place=False``, returns a molecular system with the minimized
        coordinates in the form specified by ``to_form`` (or the original form).
        When ``in_place=True``, returns None and updates ``molecular_system`` in
        place. Existing Context/Simulation inputs operate on their engine context.


    Raises
    ------
    ExecutionPlatformUnavailableError
        If a recognized execution platform is not registered by the engine.
    ArgumentChoiceError
        If a requested platform name is unknown to the selected engine.
    LibraryNotFoundError
        If the selected execution engine is not installed.

    NotImplementedError
        Raised if the requested ``engine`` is not supported.
    NotImplementedMethodError
        If detaching an existing engine input is unsupported. This is checked
        before optimization, including when an explicit output form is requested.


    Notes
    -----
    If the input is not already an ``openmm.Context`` or ``openmm.Simulation``,
    the molecular system is converted to an ``openmm.Context`` using the MolSysMT
    default attributes for any missing molecular-mechanics parameters (forcefield,
    integrator, temperature, etc.).

    The implemented OpenMM path uses LocalEnergyMinimizer's L-BFGS algorithm
    with engine default stopping settings. This public function does not expose
    tolerance or iteration-count parameters. Constrained force components need
    not all vanish. Local optimization does not guarantee the nearest or global
    minimum, thermodynamic stability, equilibrium or a stable bound complex.
    Chemistry, spatial assembly and force-field parameters must already be
    appropriate. Extract one structure explicitly for a native MolSys input.

    Existing engine inputs must satisfy the public independent-copy contract
    before an independent optimization starts. OpenMM Context/Simulation copy
    routes are currently unimplemented, so in_place=False raises before any
    optimization or input-state change. An explicit to_form or a composite
    input containing an engine object does not bypass this ownership check.
    Use a prepared native MolSys for an independent workflow, or deliberately
    request in_place=True on an existing engine object. In-place execution
    operates on its actual model/platform and returns None; no rollback is
    promised after an explicitly requested in-place engine failure.

    See Also
    --------
    molsysmt.molecular_mechanics.get_potential_energy
        Comparing energies under the same model before and after optimization.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'], structure_indices=0)
    >>> minimized = msm.molecular_mechanics.potential_energy_minimization(molsys, platform='Reference')
    >>> minimized is molsys
    False
    >>> result = msm.molecular_mechanics.potential_energy_minimization(molsys, in_place=True, platform='Reference')
    >>> result is None
    True

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Potential_energy_minimization` for independent and
       in-place native workflows, units and interpretation limits.


    .. versionadded:: 1.0.0
    """

    from molsysmt import convert, copy, get_form, set

    if engine == "OpenMM":
        from openmm import LocalEnergyMinimizer

        form_in = get_form(molecular_system)
        source_forms = form_in if isinstance(form_in, (list, tuple)) else [form_in]
        engine_input = any(
            form in ("openmm.Context", "openmm.Simulation") for form in source_forms
        )
        # Existing engine objects can be shared by conversion routes. Detach
        # them through the form's copy contract before any optimization.
        detached_input = not in_place and engine_input
        calculation_system = (
            copy(molecular_system) if detached_input else molecular_system
        )

        if form_in == "openmm.Context":
            context = calculation_system

        elif form_in == "openmm.Simulation":
            context = calculation_system.context

        else:
            from molsysmt._private.mechanical_model import context_defaults

            extra_conversion_arguments = context_defaults(molecular_system)

            context = convert(
                calculation_system,
                to_form="openmm.Context",
                **extra_conversion_arguments,
                platform=platform,
            )

        state_pre_min = context.getState(getEnergy=True)
        LocalEnergyMinimizer.minimize(context)
        state_post_min = context.getState(getEnergy=True, getPositions=True)

        if verbose:
            energy_pre_min = state_pre_min.getPotentialEnergy()
            energy_pre_min = puw.standardize(energy_pre_min)
            print("Potential Energy before minimization: {}".format(energy_pre_min))
            energy_post_min = state_post_min.getPotentialEnergy()
            energy_post_min = puw.standardize(energy_post_min)
            print("Potential Energy after minimization: {}".format(energy_post_min))

        if in_place:
            if form_in not in ["openmm.Context", "openmm.Simulation"]:
                coordinates = state_post_min.getPositions(asNumpy=True)
                set(molecular_system, coordinates=coordinates)
            pass
        else:
            if to_form is None:
                output = (
                    calculation_system if detached_input else copy(molecular_system)
                )
            else:
                output = convert(calculation_system, to_form=to_form)
            coordinates = state_post_min.getPositions(asNumpy=True)
            set(output, coordinates=coordinates)
            return output

    else:
        raise NotImplementedError
