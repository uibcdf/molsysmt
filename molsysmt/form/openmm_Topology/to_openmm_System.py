from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_openmm_System(item, atom_indices='all', forcefield='AMBER14', water_model=None, implicit_solvent=None,
        non_bonded_method=None, constraints='hbonds', switch_distance=None,
        dispersion_correction=None, ewald_error_tolerance=None, skip_digestion=False):
    """
    Converting from openmm.Topology to openmm.System.

    Parameters
    ----------
    item : openmm.Topology
        Source item in openmm.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    forcefield : object
        Argument forcefield.
    water_model : object
        Argument water_model.
    implicit_solvent : object
        Argument implicit_solvent.
    non_bonded_method : object
        Argument non_bonded_method.
    constraints : object
        Argument constraints.
    switch_distance : object
        Argument switch_distance.
    dispersion_correction : object
        Argument dispersion_correction.
    ewald_error_tolerance : object
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
        if has_pbc(item):
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

