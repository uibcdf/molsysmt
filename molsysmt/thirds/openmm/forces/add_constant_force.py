from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def add_constant_force(molecular_system, selection='all',
                       force='[500,0,0] kilojoules/(mole*nanometer)', return_force=False,
                       syntax='MolSysMT', skip_digestion=False):

    from molsysmt import select, get, get_form
    from openmm import CustomExternalForce

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    potential = "-(px*x+py*y+pz*z)"
    force = puw.convert(force, to_form='openmm.unit')

    ommforce = CustomExternalForce(potential)
    ommforce.addGlobalParameter('px', force[0])
    ommforce.addGlobalParameter('py', force[1])
    ommforce.addGlobalParameter('pz', force[2])

    for ii in atom_indices:
        ommforce.addParticle(int(ii))

    if not return_force:
        form_in = get_form(molecular_system)
        if form_in == 'openmm.Context':
            context = molecular_system
            index_force = context.getSystem().addForce(ommforce)
            context.reinitialize(preserveState=True)
            return index_force
        elif form_in == 'openmm.System':
            system = molecular_system
            index_force = system.addForce(ommforce)
            return index_force
        elif form_in == 'openmm.Simulation':
            simulation = molecular_system
            index_force = simulation.system.addForce(ommforce)
            simulation.context.reinitialize(preserveState=True)
            return index_force
    else:
        return ommforce

