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


    Newly constructed models reject stored controls that the selected adapter
    cannot apply. Inspect the supported physical recipe with
    :func:`molsysmt.molecular_mechanics.get_model_recipe`. A supplied parameterized
    engine model remains authoritative; its construction history is not inferred.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    decomposition : bool, default=False
        Return one potential-energy contribution per force.
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
        Total potential energy, or a dictionary of force labels to scalar energies.
        Quantities follow the active PyUnitWizard energy policy. Unique force
        names are kept. A repeated name includes its zero-based force index as
        ``Name [force i]``. A suffix is repeated if it collides with a literal name.


    Raises
    ------
    ExecutionPlatformUnavailableError
        If a recognized execution platform is not registered by the engine.
    ArgumentChoiceError
        If a requested platform name is unknown to the selected engine.
    LibraryNotFoundError
        If the selected execution engine is not installed.
    NotImplementedMethodError
        If per-force evaluation cannot isolate the forces in a supplied OpenMM
        Context or Simulation, or needs more than 32 groups in a constructed model.
    StructuralInconsistencyError
        If the decomposed energies cannot reproduce the finite total.

    Notes
    -----
    A supplied OpenMM Context or Simulation must already have separate force
    groups, including reciprocal-space groups that belong to a different force.
    The System's grouping must reflect the initialized Context. Set force groups
    before constructing the Context to request individual terms. This calculation
    reads the active positions, periodic box and parameters. It leaves the
    caller's force grouping intact. Direct and reciprocal contributions of
    the same force appear under one key. Models constructed for the calculation
    can use a separate evaluation Context when their groups overlap.

    .. versionadded:: 1.0.0
    """

    from molsysmt import convert, get_form

    if engine == "OpenMM":
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
            from molsysmt._private.mechanical_model import context_defaults

            extra_conversion_arguments = context_defaults(molecular_system)

            context = convert(
                molecular_system,
                to_form="openmm.Context",
                selection=selection,
                syntax=syntax,
                **extra_conversion_arguments,
                platform=platform,
            )

        if decomposition:
            from molsysmt.third_party.openmm._energy_decomposition import (
                decompose_potential_energy,
            )

            source_forms = [form_in] if isinstance(form_in, str) else form_in
            supplied = {"openmm.Context", "openmm.Simulation"}.intersection(
                source_forms
            )
            energies = decompose_potential_energy(context, constructed=not supplied)
            output = {key: puw.standardize(value) for key, value in energies.items()}

        else:
            state = context.getState(getEnergy=True)
            output = state.getPotentialEnergy()
            output = puw.standardize(output)

        return output

    else:
        raise NotImplementedError
