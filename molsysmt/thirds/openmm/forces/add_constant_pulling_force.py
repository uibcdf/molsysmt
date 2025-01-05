from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def add_constant_pulling_force(molecular_system=None, selection='all',
                               pulling_force='[500,0,0] kilojoules_per_mole/nm', adding_force=False,
                               syntax='MolSysMT', skip_digestion=False):

    from molsysmt import select, get, get_form
    from openmm import CustomExternalForce

    if molecular_system is not None:
        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    else:
        atom_indices = selection

    for atom_index in atom_indices:
        force.addParticle(int(atom_index))

    potential = "-(px*x+py*y+pz*z)"

    force = CustomExternalForce(potential)
    force.addGlobalParameter('px', pulling_force[0])
    force.addGlobalParameter('py', pulling_force[1])
    force.addGlobalParameter('pz', pulling_force[2])

    for ii in atom_indices:
        force.addParticle(int(atom_index))

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

