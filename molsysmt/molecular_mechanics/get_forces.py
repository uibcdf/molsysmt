from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest()
@dep_digest("openmm", when={"engine": "OpenMM"})
def get_forces(
    molecular_system,
    element="atom",
    selection="all",
    magnitude=False,
    engine="OpenMM",
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    structure_indices=None,
    platform="CPU",
):
    """Calculating atomic potential forces in the complete molecular environment.

    Atom selection filters the returned forces after evaluation of the complete
    model. It never removes the other atoms from the physical environment.
    Existing engine contexts are read without reconstruction. Other forms use
    the public conversion route with stored model requests before configured
    defaults, without chemical preparation, integration or minimization.

    Newly constructed models reject stored controls that the selected adapter
    cannot apply. Inspect the supported physical recipe with
    :func:`molsysmt.molecular_mechanics.get_model_recipe`. A supplied parameterized
    engine model remains authoritative; its construction history is not inferred.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to analyze in any supported form supplying coordinates
        and a model or sufficient chemistry for parameterization. A native
        MolSys may carry model requests in its MolecularMechanics domain.
    element : str, default='atom'
        Returned element level. Only atomic forces are supported; other levels
        are rejected rather than implicitly summing or averaging forces.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection: query string, 0-based indices or a full Boolean mask.
        Explicit index order and repetitions are preserved. An empty list
        returns a typed empty atom axis. See :ref:`Introduction_Selection`.
    magnitude : bool, default=False
        Return each atom's Euclidean force norm instead of its three components.
    engine : str, default='OpenMM'
        Execution engine. Only OpenMM is implemented. It supplies the actual
        potential-force calculation; no different engine is used on failure.
    syntax : str, default='MolSysMT'
        Syntax interpreting selection queries. See :ref:`Introduction_Selection`.
    skip_digestion : bool, default=False
        Skip argument digestion only for already validated internal inputs.
    structure_indices : int, list, tuple, numpy.ndarray, str, or None, default=None
        Keyword-only 0-based structure selection. None reads the first stored
        structure or the current Context/Simulation and retains the legacy
        result without a structure axis. Explicit indices, including a single
        index or 'all', retain a leading structure axis. Order and repetitions
        are preserved; an empty list returns a typed empty structure axis.
        A Context/Simulation contains only its current structure, at index 0.
    platform : str, default='CPU'
        Keyword-only execution platform for newly constructed contexts. Existing
        Context/Simulation inputs keep their actual platform and parameters.
        Engine platform validation is delegated to the existing adapter.

    Returns
    -------
    quantity
        Forces in the application's PyUnitWizard standard units, normally
        kJ/(mol*nm). With structure_indices=None, vector shape is (n_atoms, 3)
        and magnitude shape is (n_atoms,). An explicit structure selection gives
        (n_structures, n_atoms, 3) or (n_structures, n_atoms), respectively.
        Result arrays are detached from the molecular system and engine state.

    Raises
    ------
    ArgumentError
        If a positional population is invalid or outside the corresponding axis.
    ArgumentChoiceError
        If the engine or returned element level is not supported.
    ArgumentConflictError
        If selected structures do not share the declared reference chemical state.
    NotWithThisFormError
        If coordinates are absent. Incomplete chemical models retain their
        conversion or engine parameterization diagnostic and original cause.
    NotImplementedMethodError
        If a declared mechanical override has no supported construction route,
        or a composite input contains an existing Context/Simulation.
    MemoryBudgetExceededError
        If resident output plus one numerical work block exceeds the budget.
    UnsupportedHeavyOperationError
        If a large coordinate source has no declared streaming route.
    LibraryNotFoundError
        If the requested optional execution engine is unavailable.

    Notes
    -----
    - Forces are OpenMM's raw potential gradients, not constraint reaction
      forces, impulses or accelerations. Reading does not apply constraints,
      advance time, repair chemistry, add particles or optimize coordinates.
    - A stored force-field name is a model request, not a preparameterized
      System. Construction uses the existing forcefield, water_model,
      implicit_solvent, constraints, non_bonded_method, switch_distance,
      dispersion_correction and ewald_error_tolerance conversion contract.
      Unsupported stored overrides are refused explicitly. Supply an existing
      Context/Simulation for a custom already-parameterized model.
    - Periodic evaluation uses the model's method and each structure's box,
      whose vectors are rows. Native construction uses the reference chemical
      state; a conflicting or unknown multi-state association is rejected.
      A supplied System is already parameterized and needs no chemical-state
      reconstruction; its fixed default box is used if structural data lacks
      boxes. Supplied model/coordinate axes must correspond explicitly.
    - Coordinate streaming uses ChunkedExecutor where supported. Output stays
      resident and must fit the numerical memory estimate; engine allocations,
      caller-owned arrays and process RSS are outside that estimate.
    - Completed engine execution is credited through optional Ackredit capture.
      Attribution and scientific profiles are distinct from release qualification.

    See Also
    --------
    molsysmt.molecular_mechanics.get_potential_energy
        Evaluate the potential energy of a declared molecular model.
    molsysmt.basic.convert
        Construct an engine representation using supported model requests.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    >>> molsys = msm.convert(source, structure_indices=0)
    >>> forces = msm.molecular_mechanics.get_forces(molsys, platform='Reference')
    >>> forces.shape
    (22, 3)
    >>> msm.molecular_mechanics.get_forces(
    ...     molsys, selection=[0], structure_indices=[0], platform='Reference').shape
    (1, 1, 3)

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Get_forces` for model, selection and structure examples.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.molecular_forces import calculate
    from molsysmt._private.smonitor import ArgumentChoiceError

    caller = "molsysmt.molecular_mechanics.get_forces"
    if element != "atom":
        raise ArgumentChoiceError("element", element, ["atom"], caller=caller)
    if engine != "OpenMM":
        raise ArgumentChoiceError("engine", engine, ["OpenMM"], caller=caller)
    return calculate(
        molecular_system,
        selection=selection,
        structure_indices=structure_indices,
        magnitude=magnitude,
        platform=platform,
        syntax=syntax,
    )
