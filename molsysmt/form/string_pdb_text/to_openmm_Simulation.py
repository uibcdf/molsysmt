from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_openmm_Simulation(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:pdb_text to openmm.Simulation.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Simulation
        Resulting object in openmm.Simulation form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Modeller.to_openmm_Modeller import to_openmm_Modeller
    from molsysmt.form.openmm_Modeller.to_openmm_Simulation import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

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

