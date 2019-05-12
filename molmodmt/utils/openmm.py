
def check_platforms():

    from simtk.openmm import Platform as _Platform

    for ii in range(_Platform.getNumPlatforms()):
        platform_name  = _Platform.getPlatform(ii).getName()
        platform       = _Platform.getPlatformByName(platform_name)
        platform_speed = platform.getSpeed()
        print('Plataforma {} con velocidad {}'.format(platform_name,platform_speed))
    del(platform_name, platform, platform_speed, _Platform)


def add_harmonic_restraint_in_absolute_positions (system=None, atoms_list=None, K=None,
                                                  positions=None):
    #50.0 * unit.kilocalories_per_mole/unit.angstrom**2

    from simtk.openmm import CustomExternalForce
    from simtk.unit import md_unit_system

    harmonic_restraint_potential = "0.5*K*((x-xo)^2 + (y-yo)^2 + (z-zo)^2)"
    force = CustomExternalForce(harmonic_restraint_potential)
    force.addGlobalParameter('K', K)
    force.addPerParticleParameter('xo')
    force.addPerParticleParameter('yo')
    force.addPerParticleParameter('zo')

    for ii in range(len(atoms_list)):
        atom_index = atoms_list[ii]
        atom_position = positions[ii].value_in_unit_system(md_unit_system)
        force.addParticle(int(atom_index), atom_position)

    system.addForce(force)

    pass

def add_harmonic_restraint_in_relative_positions (system=None, atoms_pairs_list=None, K=None,
                                                 relative_positions=None,
                                                 system_positions=None):

    harmonic_restraint_vector_potential = "0.5*K*( (x2-x1-vx)^2 + (y2-y1-vy)^2 + (z2-z1-vz)^2)"
    force = CustomCompoundBondForce(2,harmonic_restraint_vector_potential)
    force.addGlobalParameter('K', K)
    force.addPerBondParameter('vx')
    force.addPerBondParameter('vy')
    force.addPerBondParameter('vz')

    if system_positions is not None:
        for atoms_pair in atoms_pair_list:
            atom_a, atom_b = atoms_pair
            position_a = system_positions[atom_a].value_in_unit_system(md_unit_system)
            position_b = system_positions[atom_b].value_in_unit_system(md_unit_system)
            vector_b_a = position_b - position_a
            force.addBond([int(atom_a),int(atom_b)], vector_b_a)

    system.addForce(force)

    pass

def add_harmonic_restraint_in_distances (system=None, atoms_pairs_list=None, K=None,
                                         distances=None):

    from simtk.openmm import HarmonicBondForce
    from simtk.unit import md_unit_system

    force = HarmonicBondForce()

    for ii in range(len(atoms_list)):
        atom_a, atom_b = atoms_pairs_list[ii]
        dist_a_b = distances[ii].value_in_unit_system(md_unit_system)
        force.addBond(int(atom_a), int(atom_b), dist_a_b, K)

    system.addForce(force)

    pass

def add_constant_pulling_force (system=None, atoms_list=None, pulling_force=None):

    from simtk.openmm import CustomExternalForce

    if type(atoms_list) in [int]:
        atoms_list = [atoms_list]

    pulling_potential = "-(px*x+py*y+pz*z)"
    force = CustomExternalForce(pulling_potential)
    force.addGlobalParameter('px', pulling_force[0])
    force.addGlobalParameter('py', pulling_force[1])
    force.addGlobalParameter('pz', pulling_force[2])

    for atom_index in atoms_list:
        force.addParticle(int(atom_index))

    system.addForce(force)

    pass
