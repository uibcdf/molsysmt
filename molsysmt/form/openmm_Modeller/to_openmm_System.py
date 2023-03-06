from molsysmt._private.digestion import digest

@digest(form='openmm.Modeller')
def to_openmm_System(item, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = openmm_Topology_to_openmm_System(tmp_item, forcefield=forcefield,
                                                non_bonded_method=non_bonded_method, non_bonded_cutoff=non_bonded_cutoff,
                                                constraints=constraints, rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                                                hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                                                flexible_constraints=flexible_constraints,
                                                **kwargs)

    return tmp_item

def _to_openmm_System(item, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    return to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                            forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm',
                                            constraints=None,
                                            rigid_water=True, remove_cm_motion=True, hydrogen_mass=None,
                                            switch_distance=None,
                                            flexible_constraints=False)

