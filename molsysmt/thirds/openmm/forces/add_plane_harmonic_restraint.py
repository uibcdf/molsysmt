from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def add_plane_harmonic_restraint(molecular_system=None, selection='all', force_constant='5000 kilojoules/(mol*nanometers**2)',
        point=None, vector=[0,0,1], pbc=False, return_force=False, syntax='MolSysMT', skip_digestion=False):

    from molsysmt import select, get, get_form
    from openmm import CustomExternalForce
    from openmm import unit as u

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    force_constant = puw.convert(force_constant, to_form='openmm.unit')

    if pbc:
        potential = (
            "0.5 * k * (r^2); "
            "r = abs(periodicdistance(a, b, c, 0, 0, 0)); "
            "a = u * vx; "
            "b = u * vy; "
            "c = u * vz; "
            "u = (x - px) * vx + (y - py) * vy + (z - pz) * vz;"
        )
    else:
        potential = (
            "0.5 * k * (a^2+b^2+c^2); "
            "a = u * vx; "
            "b = u * vy; "
            "c = u * vz; "
            "u = (x - px) * vx + (y - py) * vy + (z - pz) * vz;"
        )

    if point is None:

        coordinates_minimum = get(molecular_system, element='atom', selection=atom_indices,
                    coordinates=True)
        coordinates_minimum = puw.convert(coordinates_minimum[0], to_form='openmm.unit')

        force = CustomExternalForce(potential)
        force.addGlobalParameter('k', force_constant)
        force.addGlobalParameter('vx', vector[0])
        force.addGlobalParameter('vy', vector[1])
        force.addGlobalParameter('vz', vector[2])
        force.addPerParticleParameter('px')
        force.addPerParticleParameter('py')
        force.addPerParticleParameter('pz')

        n_atoms_in_coordinates_minimum = coordinates_minimum.shape[0]

        if n_atoms_in_coordinates_minimum == 1:
            for ii, atom_index in enumerate(atom_indices):
                force.addParticle(atom_index, coordinates_minimum[0])
        else:
            for ii, atom_index in enumerate(atom_indices):
                force.addParticle(atom_index, coordinates_minimum[ii])

    else:

        point = puw.convert(point, to_unit=u.nanometer, to_form='openmm.unit')[0]

        print(point)

        force = CustomExternalForce(potential)
        force.addGlobalParameter('k', force_constant)
        force.addGlobalParameter('vx', vector[0])
        force.addGlobalParameter('vy', vector[1])
        force.addGlobalParameter('vz', vector[2])
        force.addGlobalParameter('px', point[0])
        force.addGlobalParameter('py', point[1])
        force.addGlobalParameter('pz', point[2])

        for atom_index in atom_indices:
            force.addParticle(atom_index)

    if not return_force:
        form_in = get_form(molecular_system)
        if form_in == 'openmm.Context':
            context = molecular_system
            index_force = context.getSystem().addForce(force)
            context.reinitialize(preserveState=True)
            return index_force
        elif form_in == 'openmm.System':
            system = molecular_system
            index_force = system.addForce(force)
            return index_force
        elif form_in == 'openmm.Simulation':
            simulation = molecular_system
            index_force = simulation.system.addForce(force)
            simulation.context.reinitialize(preserveState=True)
            return index_force
    else:
        return force

