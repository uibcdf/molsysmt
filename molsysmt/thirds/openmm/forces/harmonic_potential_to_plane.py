from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def harmonic_potential_to_plane(molecular_system=None, selection='all', force_constant=None,
        point=None, normal_vector=None, pbc=False, adding_force=False, syntax='MolSysMT'):

    from molsysmt import select, get, get_form
    from openmm import CustomExternalForce

    if molecular_system is not None:
        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    else:
        atom_indices = selection

    if coordinates_minimum is None:
        if molecular_system is not None:
            coordinates_minimum = get(molecular_system, element='atom', selection=atom_indices,
                    coordinates=True)

    force_constant = puw.convert(force_constant, to_form='openmm.unit')
    coordinates_minimum = puw.convert(coordinates_minimum[0], to_form='openmm.unit')


    # Add a restrining potential to keep atoms in z=0

    if np.isclose(normal_vector, [1.0, 0.0, 0.0]):

        if pbc:
            potential = '0.5 * k * (r^2); \
                    r = periodicdistance(x, y, z, px, y, z);'
        else:
            potential = '0.5 * k * (r^2); \
                    r = (x - px);'

        force = CustomExternalForce(potential)
        force.addGlobalParameter('k', force_constant)
        force.addGlobalParameter('px', point[0])

    elif np.isclose(normal_vector, [0.0, 1.0 , 0.0]):

        if pbc:
            potential = '0.5 * k * (r^2); \
                    r = periodicdistance(x, y, z, x, py, z);'
        else:
            potential = '0.5 * k * (r^2); \
                    r = (y - py);'

        force = CustomExternalForce(potential)
        force.addGlobalParameter('k', force_constant)
        force.addGlobalParameter('py', point[1])

    elif np.isclose(normal_vector, [0.0, 0.0, 1.0]):

        if pbc:
            potential = '0.5 * k * (r^2); \
                    r = periodicdistance(x, y, z, x, y, pz);'
        else:
            potential = '0.5 * k * (r^2); \
                    r = (z - pz);'

        force = CustomExternalForce(potential)
        force.addGlobalParameter('k', force_constant)
        force.addGlobalParameter('pz', point[2])

    else:

        if pbc:
            potential = '0.5 * k * (r^2); \
                r = abs(periodicdistance(a, b, c, 0, 0, 0)); \
                a = u*vx; \
                b = u*vy; \
                c = u*vz; \
                u = (x-px)*vx+(y-py)*vy+(z-pz)*vz;'
        else:
            potential = '0.5 * k * (a^2+b^2+c^2); \
                a = u*vx; \
                b = u*vy; \
                c = u*vz; \
                u = (x-px)*vx+(y-py)*vy+(z-pz)*vz;'

        force = CustomExternalForce(potential)
        force.addGlobalParameter('k', force_constant)
        force.addGlobalParameter('px', point[0])
        force.addGlobalParameter('py', point[1])
        force.addGlobalParameter('pz', point[2])
        force.addGlobalParameter('vx', normal_vector[0])
        force.addGlobalParameter('vy', normal_vector[1])
        force.addGlobalParameter('vz', normal_vector[2])

    for atom_index in atom_indices:
        force.addParticle(atom_index)

    if adding_force:
        form_in = get_form(molecular_system)
        if form_in == 'openmm.Context':
            context = molecular_system
            index_force = context.getSystem().addForce(force)
            aux_positions = context.getState(getPositions=True).getPositions()
            aux_velocities = context.getState(getVelocities=True).getVelocities()
            context.reinitialize()
            context.setPositions(aux_positions)
            context.setVelocities(aux_velocities)
            return index_force
        elif form_in == 'openmm.System':
            system = molecular_system
            index_force = system.addForce(force)
            return index_force
    else:
        return force

