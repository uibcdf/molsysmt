from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.Topology")
@dep_digest("openmm")
def to_openmm_System(
    item,
    atom_indices="all",
    forcefield="AMBER14",
    water_model=None,
    implicit_solvent=None,
    non_bonded_method=None,
    constraints="hbonds",
    switch_distance=None,
    dispersion_correction=None,
    ewald_error_tolerance=None,
    skip_digestion=False,
):
    """
    Converting from openmm.Topology to openmm.System.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    forcefield : str, default='AMBER14'
        Force field parameter identifier or name.
    water_model : str, default=None
        Water model parameter identifier (e.g., 'TIP3P').
    implicit_solvent : str, default=None
        OpenMM implicit-solvent model: 'OBC1' (Amber igb=2) or 'OBC2'
        (igb=5). Uses OpenMM's corresponding implicit XML, mbondi2 radii,
        ACE surface term and default dielectric/screening parameters.
        Takes precedence over water_model. By default, no implicit model.
    non_bonded_method : object, default=None
        OpenMM nonbonded method or its name. Implicit solvent admits
        NoCutoff, CutoffNonPeriodic and CutoffPeriodic; its default is
        NoCutoff even when a box is present. PME/Ewald/LJPME are refused.
    constraints : object, default='hbonds'
        Physical constraint policy: None/'none', 'hbonds', 'all bonds' or
        'h angles'. The adapter translates these names to engine constants.
    switch_distance : object, default=None
        Argument switch_distance.
    dispersion_correction : object, default=None
        Argument dispersion_correction.
    ewald_error_tolerance : object, default=None
        Argument ewald_error_tolerance.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.System
        Resulting object in openmm.System form.

    Notes
    -----
    OBC I and II are the distinct Onufriev-Bashford-Case parameterizations
    (2004), DOI 10.1002/prot.20033, executed faithfully through OpenMM's
    shipped XML definitions. This is not a MolSysMT GB reimplementation.
    Successful construction contributes the method and executed OpenMM
    version to optional Ackredit tracking. Applications own capture sessions;
    OpenMM XML serialization does not preserve that separate bibliography.

    .. versionadded:: 1.0.0
    """

    import openmm
    from openmm import app

    from molsysmt._private.smonitor import ArgumentChoiceError
    from molsysmt.molecular_mechanics import get_engine_forcefield

    resources = get_engine_forcefield(
        forcefield,
        water_model=water_model,
        implicit_solvent=implicit_solvent,
        engine="OpenMM",
        skip_digestion=True,
    )

    if implicit_solvent is not None:
        methods = {
            "nocutoff": app.NoCutoff,
            "cutoffnonperiodic": app.CutoffNonPeriodic,
            "cutoffperiodic": app.CutoffPeriodic,
        }
        if non_bonded_method is None:
            non_bonded_method = app.NoCutoff
        elif isinstance(non_bonded_method, str):
            key = (
                non_bonded_method.lower()
                .replace(" ", "")
                .replace("_", "")
                .replace("-", "")
            )
            non_bonded_method = methods.get(key, non_bonded_method)
        if non_bonded_method not in methods.values():
            raise ArgumentChoiceError(
                "non_bonded_method",
                non_bonded_method,
                ["NoCutoff", "CutoffNonPeriodic", "CutoffPeriodic"],
                caller="molsysmt.form.openmm_Topology.to_openmm_System",
            )
    elif non_bonded_method is None:
        from molsysmt.form.openmm_Topology.has_attribute import has_attribute

        if has_attribute(item, "box"):
            non_bonded_method = "PME"
        else:
            non_bonded_method = "no cutoff"
        non_bonded_method = app.CutoffNonPeriodic

    if non_bonded_method == "no cutoff":
        non_bonded_method = app.NoCutoff
    elif non_bonded_method == "PME":
        non_bonded_method = app.PME

    policies = {
        "none": None,
        "noconstraints": None,
        "hbonds": app.HBonds,
        "allbonds": app.AllBonds,
        "hangles": app.HAngles,
    }
    if isinstance(constraints, str):
        key = constraints.lower().replace(" ", "").replace("_", "").replace("-", "")
        if key not in policies:
            raise ArgumentChoiceError(
                "constraints",
                constraints,
                [None, "hbonds", "all bonds", "h angles"],
                caller="molsysmt.form.openmm_Topology.to_openmm_System",
            )
        constraints = policies[key]
    elif constraints not in policies.values():
        raise ArgumentChoiceError(
            "constraints",
            constraints,
            [None, "hbonds", "all bonds", "h angles"],
            caller="molsysmt.form.openmm_Topology.to_openmm_System",
        )

    engine_forcefield = app.ForceField(*resources)
    system = engine_forcefield.createSystem(
        item, nonbondedMethod=non_bonded_method, constraints=constraints
    )

    if dispersion_correction or ewald_error_tolerance:
        forces = {ii.__class__.__name__: ii for ii in system.getForces()}
    if dispersion_correction:
        forces["NonbondedForce"].setUseDispersionCorrection(True)
    if ewald_error_tolerance:
        forces["NonbondedForce"].setEwaldErrorTolerance(ewald_error_tolerance)

    from molsysmt._private.scientific_attribution import credit_implicit_solvent

    credit_implicit_solvent(
        implicit_solvent,
        "openmm",
        openmm.__version__,
        "molsysmt.form.openmm_Topology.to_openmm_System",
        forcefield=forcefield,
        resources=resources,
    )
    return system
