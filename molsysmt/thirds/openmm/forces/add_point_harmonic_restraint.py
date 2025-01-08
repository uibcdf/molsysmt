from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def add_point_harmonic_restraint(molecular_system, selection='all', force_constant='5000 kilojoules/(mol*nanometers**2)',
        point=None, pbc=False, return_force=False, syntax='MolSysMT', skip_digestion=False):

    from molsysmt import select, get, get_form
    from openmm import CustomExternalForce
    from openmm import unit as u

    form_in = get_form(molecular_system)

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if point is None:
        if form_in=='openmm.Context':
            raise ValueError("A point must be provided when the input is an OpenMM Context object.")
        else:
            point = get(molecular_system, element='atom', selection=atom_indices, coordinates=True)[0]

    force_constant = puw.convert(force_constant, to_unit=u.kilojoule_per_mole/(u.nanometer**2), to_form='openmm.unit')
    point = puw.convert(point, to_unit=u.nanometer, to_form='openmm.unit')

    if pbc:
        potential = "0.5*k*periodicdistance(x, y, z, x0, y0, z0)^2"
    else:
        potential = "0.5*k*((x-x0)^2 + (y-y0)^2 + (z-z0)^2)"

    force = CustomExternalForce(potential)
    force.addGlobalParameter('k', force_constant)
    force.addPerParticleParameter('x0')
    force.addPerParticleParameter('y0')
    force.addPerParticleParameter('z0')

    n_atoms_in_point = point.shape[0]

    if n_atoms_in_point == 1:
        for ii, atom_index in enumerate(atom_indices):
            force.addParticle(atom_index, point[0])
    else:
        for ii, atom_index in enumerate(atom_indices):
            force.addParticle(atom_index, point[ii])

    if not return_force:
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
        elif form_in == 'openmm.Simulation':
            simulation = molecular_system
            index_force = simulation.system.addForce(force)
            simulation.context.reinitialize(preserveState=True)
            return index_force
    else:
        return force

