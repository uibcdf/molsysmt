from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_openmm_System(item, atom_indices='all', forcefield='AMBER14', water_model=None, implicit_solvent=None,
        non_bonded_method=None, constraints='hbonds', switch_distance=None,
        dispersion_correction=None, ewald_error_tolerance=None, skip_digestion=False):

    from openmm import app
    from molsysmt.molecular_mechanics import forcefield_to_engine

    forcefield = forcefield_to_engine(forcefield,
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

