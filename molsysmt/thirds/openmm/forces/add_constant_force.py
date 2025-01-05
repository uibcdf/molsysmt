from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def add_constant_force(molecular_system=None, selection='all',
                       force='[500,0,0] kilojoules/(mole*nanometer)', return_force=False,
                       syntax='MolSysMT', skip_digestion=False):

    from molsysmt import select, get, get_form
    from openmm import CustomExternalForce

    if molecular_system is not None:
        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    else:
        atom_indices = selection

    potential = "-(px*x+py*y+pz*z)"

    ommforce = CustomExternalForce(potential)
    ommforce.addGlobalParameter('px', pulling_force[0])
    ommforce.addGlobalParameter('py', pulling_force[1])
    ommforce.addGlobalParameter('pz', pulling_force[2])

    for ii in atom_indices:
        ommforce.addParticle(int(atom_index))

    if adding_force:
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

