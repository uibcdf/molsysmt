from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_openmm_System(item, atom_indices='all', forcefield='AMBER14', water_model=None, implicit_solvent=None,
        non_bonded_method=None, constraints='hbonds', switch_distance=None,
        dispersion_correction=None, ewald_error_tolerance=None, skip_digestion=False):
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
        Implicit solvent model name if applicable.
    non_bonded_method : object, default=None
        Argument non_bonded_method.
    constraints : object, default='hbonds'
        Argument constraints.
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


    .. versionadded:: 1.0.0
    """

    from openmm import app
    from molsysmt.molecular_mechanics import get_engine_forcefield

    forcefield = get_engine_forcefield(forcefield,
                 water_model=water_model, implicit_solvent=implicit_solvent,
                 engine='OpenMM', skip_digestion=True)

    forcefield = app.ForceField(*forcefield)

    if non_bonded_method is None:
        from molsysmt.form.openmm_Topology.has_attribute import has_attribute
        if has_attribute(item, 'box'):
            non_bonded_method = 'PME'
        else:
            non_bonded_method = 'no cutoff'
        non_bonded_method=app.CutoffNonPeriodic

    if non_bonded_method=='no cutoff':
        non_bonded_method=app.NoCutoff
    elif non_bonded_method=='PME':
        non_bonded_method=app.PME

    if constraints=='hbonds':
        contraints=app.HBonds

    system = forcefield.createSystem(item, nonbondedMethod=non_bonded_method, constraints=app.HBonds)

    if dispersion_correction or ewald_error_tolerance:
        forces = {ii.__class__.__name__ : ii for ii in system.getForces()}
    if dispersion_correction:
        forces['NonbondedForce'].setUseDispersionCorrection(True)
    if ewald_error_tolerance:
        forces['NonbondedForce'].setEwaldErrorTolerance(ewald_error_tolerance)

    return system

