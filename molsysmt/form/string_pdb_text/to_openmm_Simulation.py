from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_openmm_Simulation(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import to_openmm_Modeller
    from ..openmm_Modeller import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

    tmp_item = to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = openmm_Modeller_to_openmm_Simulation(tmp_item, skip_digestion=True)

    return tmp_item

#    tmp_item, tmp_molecular_system = openmm_Modeller_to_openmm_Simulation(tmp_item, molecular_system=tmp_molecular_system, forcefield=forcefield, non_bonded_method=non_bonded_method,
#                                                    non_bonded_cutoff=non_bonded_cutoff, constraints=constraints, rigid_water=rigid_water,
#                                                    remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass,
#                                                    switch_distance=switch_distance, flexible_constraints=flexible_constraints,
#                                                    integrator=integrator, temperature=temperature,
#                                                    collisions_rate=collisions_rate, integration_timestep=integration_timestep,
#                                                    platform=platform, **kwargs)
#

