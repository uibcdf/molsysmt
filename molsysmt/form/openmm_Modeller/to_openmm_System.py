from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Modeller')
def to_openmm_System(item, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False, skip_digestion=False):
    """
    Converting from openmm.Modeller to openmm.System.

    Parameters
    ----------
    item : openmm.Modeller
        Source item in openmm.Modeller form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    forcefield : object
        Argument forcefield.
    non_bonded_method : object
        Argument non_bonded_method.
    non_bonded_cutoff : object
        Argument non_bonded_cutoff.
    constraints : object
        Argument constraints.
    rigid_water : object
        Argument rigid_water.
    remove_cm_motion : object
        Argument remove_cm_motion.
    hydrogen_mass : object
        Argument hydrogen_mass.
    switch_distance : object
        Argument switch_distance.
    flexible_constraints : object
        Argument flexible_constraints.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.System
        Resulting object in openmm.System form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_openmm_System import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = openmm_Topology_to_openmm_System(tmp_item, forcefield=forcefield,
                                                non_bonded_method=non_bonded_method, non_bonded_cutoff=non_bonded_cutoff,
                                                constraints=constraints, rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                                                hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                                                flexible_constraints=flexible_constraints, skip_digestion=True)

    return tmp_item

