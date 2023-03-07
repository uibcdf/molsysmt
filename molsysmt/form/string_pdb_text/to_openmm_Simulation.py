from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_openmm_Simulation(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_Modeller
    from ..openmm_Modeller import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

    tmp_item = to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = openmm_Modeller_to_openmm_Simulation(tmp_item)

    return tmp_item

#    tmp_item, tmp_molecular_system = openmm_Modeller_to_openmm_Simulation(tmp_item, molecular_system=tmp_molecular_system, forcefield=forcefield, non_bonded_method=non_bonded_method,
#                                                    non_bonded_cutoff=non_bonded_cutoff, constraints=constraints, rigid_water=rigid_water,
#                                                    remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass,
#                                                    switch_distance=switch_distance, flexible_constraints=flexible_constraints,
#                                                    integrator=integrator, temperature=temperature,
#                                                    collisions_rate=collisions_rate, integration_timestep=integration_timestep,
#                                                    platform=platform, **kwargs)
#

def _to_openmm_Simulation(item, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):

    return to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices)

