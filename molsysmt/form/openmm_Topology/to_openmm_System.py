from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_openmm_System(item, atom_indices='all', forcefield=None, water_model=None, implicit_solvent=None,
        non_bonded_method='no cutoff', switch_distance=None, digest=True):

    forcefield = molecular_mechanics.to_openmm_ForceField()
    system_parameters = molecular_mechanics.get_openmm_System_parameters()
    tmp_item = forcefield.createSystem(item, **parameters)

    if molecular_mechanics.use_dispersion_correction or molecular_mechanics.ewald_error_tolerance:
        forces = {ii.__class__.__name__ : ii for ii in tmp_item.getForces()}
    if molecular_mechanics.use_dispersion_correction:
        forces['NonbondedForce'].setUseDispersionCorrection(True)
    if molecular_mechanics.ewald_error_tolerance:
        forces['NonbondedForce'].setEwaldErrorTolerance(molecular_mechanics.ewald_error_tolerance)

    return tmp_item
