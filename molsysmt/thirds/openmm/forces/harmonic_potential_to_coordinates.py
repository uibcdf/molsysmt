from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def harmonic_potential_to_coordinates(molecular_system=None, selection='all', force_constant=None,
        coordinates_minimum=None, pbc=False, adding_force=False, syntax='MolSysMT'):

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

    if pbc:
        potential = "0.5*k*periodicdistance(x, y, z, x0, y0, z0)^2"
    else:
        potential = "0.5*k*((x-x0)^2 + (y-y0)^2 + (z-z0)^2)"

    force = CustomExternalForce(potential)
    force.addGlobalParameter('k', force_constant)
    force.addPerParticleParameter('x0')
    force.addPerParticleParameter('y0')
    force.addPerParticleParameter('z0')

    n_atoms_in_coordinates_minimum = coordinates_minimum.shape[0]

    if n_atoms_in_coordinates_minimum == 1:
        for ii, atom_index in enumerate(atom_indices):
            force.addParticle(atom_index, coordinates_minimum[0])
    else:
        for ii, atom_index in enumerate(atom_indices):
            force.addParticle(atom_index, coordinates_minimum[ii])

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

