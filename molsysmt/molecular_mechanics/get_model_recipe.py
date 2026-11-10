"""Inspect effective physical models without creating an execution context."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "molecular_mechanics"])
@arg_digest()
@dep_digest("openmm", when={"engine": "OpenMM"})
def get_model_recipe(
    molecular_system,
    structure_indices=None,
    engine="OpenMM",
    skip_digestion=False,
):
    """Inspecting the effective recipe of a molecular-mechanics model.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying chemistry and model-construction context,
        or an already parameterized engine System, Context or Simulation.
        No atoms, hydrogens or missing chemistry are prepared implicitly.
    structure_indices : int, list, tuple or numpy.ndarray, default=None
        One structure supplying the construction box/state context. None uses
        the first stored structure, or permits coordinate-free chemistry.
        Parameterized System/Context/Simulation inputs require None and supply
        their own physical model. No trajectory
        observables or dynamics are computed.
    engine : str, default='OpenMM'
        Execution adapter whose model is inspected. OpenMM is implemented;
        model controls remain named independently of its constructor keywords.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    dict
        Detached molsysmt.model_recipe@1 record with requested values/origins,
        consumed controls, actual compiled nonbonded settings and constraint
        count, periodic box rows, engine/version, resource names and attribution. Length quantities
        use the active PyUnitWizard policy. Supplied parameterized models retain
        unknown construction provenance rather than inventing a force field.

    Raises
    ------
    NotImplementedMethodError
        If the adapter is unavailable or a stored control has no supported
        construction route. Unsupported fields are not silently ignored.
    ArgumentError
        If structure scope is invalid or contains multiple structures.
    LibraryNotFoundError
        If the selected optional engine is unavailable.

    Notes
    -----
    This experimental query parameterizes a System when necessary and inspects
    its actual engine properties, without constructing a Context, selecting a
    device, creating an integrator, minimizing or advancing coordinates.
    Execution settings such as temperature, friction and time step are outside
    this physical-model recipe. Construction can require substantial provider
    memory; no process-RSS limit or cancellation is implied.

    The supported/unsupported control sets describe the current adapter, not
    universal engine capabilities. Independent dielectric/screening/salt/cutoff,
    mass-repartitioning, rigid-water/flexible-constraint and per-atom overrides
    currently refuse. Built-in solvent-model defaults are distinguished from
    independently tunable fields. A declared implicit model deactivates a
    conflicting global explicit-water default (origin inapplicable_default),
    without editing that default or the source. Competing stored/explicit
    solvent families refuse. Legacy MolecularMechanics.formal_charge is not a
    force-field parameter; ChemicalStates formal charges remain chemistry.

    Nonbonded properties are configured engine values; a stored Ewald tolerance,
    reaction-field dielectric or dispersion flag need not be active for the
    reported nonbonded method. Default box vectors are rows, present only for a
    periodic model. Existing parameterized models can contain
    custom terms; provider force types are retained, but this compact report
    neither enumerates all particle parameters nor reconstructs arbitrary forces.
    Preserve that original model separately for exact reproduction.

    See Also
    --------
    molsysmt.molecular_mechanics.get_engine_forcefield
        Looking up model resource names without parameterization.
    molsysmt.molecular_mechanics.get_forces
        Computing potential forces with the chosen model and execution platform.

    Examples
    --------
    >>> import molsysmt as msm
    >>> model = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    >>> recipe = msm.molecular_mechanics.get_model_recipe(model)
    >>> recipe['effective']['n_particles']
    22

    .. admonition:: User guide

       See :ref:`Tutorial_Get_model_recipe` for construction and provenance limits.

    .. versionadded:: 1.0.0
    """
    from molsysmt import _ackredit
    from molsysmt._private.mechanical_model import make_recipe

    caller = "molsysmt.molecular_mechanics.get_model_recipe"
    with _ackredit.scope(caller) as provider:
        result = make_recipe(molecular_system, structure_indices, engine)
        _ackredit.credit(
            provider,
            result["attribution"]["items"],
            caller,
            contextual=True,
            context={
                "operation": "physical_model_inspection",
                "resources": result["resources"],
            },
        )
    return result
