def HarmonicRestraintPositions (atom_indices=None, K=None, positions=None):
    #2.5 * unit.kilocalories_per_mole/unit.angstrom**2

    from openmm import CustomExternalForce
    from openmm.unit import md_unit_system

    harmonic_restraint_potential = "0.5*K*((x-xo)^2 + (y-yo)^2 + (z-zo)^2)"
    force = CustomExternalForce(harmonic_restraint_potential)
    force.addGlobalParameter('K', K)
    force.addPerParticleParameter('xo')
    force.addPerParticleParameter('yo')
    force.addPerParticleParameter('zo')

    for atom_index, atom_position in zip(atom_indices, positions):
        force.addParticle(int(atom_index), atom_position.value_in_unit_system(md_unit_system))

    return force

def HarmonicRestraintDistances (atoms_pairs_list=None, K=None,
                                distances=None, system_positions=None):

    from openmm import HarmonicBondForce
    from openmm.unit import md_unit_system
    from numpy import sqrt

    force = HarmonicBondForce()

    if system_positions is not None:
        for atoms_pair in atoms_pairs_list:
            atom_a, atom_b = atoms_pair
            position_a = system_positions[atom_a].value_in_unit_system(md_unit_system)
            position_b = system_positions[atom_b].value_in_unit_system(md_unit_system)
            vect_ab = position_b - position_a
            dist_ab = sqrt(vect_ab[0]**2+vect_ab[1]**2+vect_ab[2]**2)
            force.addBond(int(atom_a), int(atom_b), dist_ab, K)

    return force

def ConstantPullingForce (atom_indices=None, pulling_force=None):

    from openmm import CustomExternalForce

    if not hasattr(atom_indices,'__iter__'):
        atom_indices = [atom_indices]

    pulling_potential = "-(px*x+py*y+pz*z)"
    force = CustomExternalForce(pulling_potential)
    force.addGlobalParameter('px', pulling_force[0])
    force.addGlobalParameter('py', pulling_force[1])
    force.addGlobalParameter('pz', pulling_force[2])

    for atom_index in atom_indices:
        force.addParticle(int(atom_index))

    return force

