def to_openmm_System (item, molecular_system=None, atom_indices='all', frame_indices='all',
                      forcefield=None,
                      non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                      rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                      flexible_constraints=False, **kwargs):

    from .openmm_Topology import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)

    tmp_item = openmm_Topology_to_openmm_System(tmp_item, atom_indices='all',
        forcefield=forcefield, non_bonded_method=non_bonded_method,
        non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
        rigid_water=rigid_water, remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass,
        switch_distance=switch_distance, flexible_constraints=flexible_constraints, **kwargs)

    return tmp_item

