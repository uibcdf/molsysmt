from molsysmt._private.digestion import digest

@digest(form='openmm.Modeller')
def to_openmm_Simulation(item, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs',
                         platform='CUDA', skip_digestion=False):

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom
    from ..openmm_Topology import to_openmm_Simulation as openmm_Topology_to_openmm_Simulation

    tmp_item  = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                   skip_digestion=True)
    positions = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                          skip_digestion=True)
    tmp_item = openmm_Topology_to_openmm_Simulation(tmp_item, forcefield=forcefield, non_bonded_method=non_bonded_method,
                                                    non_bonded_cutoff=non_bonded_cutoff, constraints=constraints, rigid_water=rigid_water,
                                                    remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                                                    flexible_constraints=flexible_constraints, integrator=integrator, temperature=temperature,
                                                    collisions_rate=collisions_rate, platform=platform,
                                                    skip_digestion=True)

    return tmp_item

