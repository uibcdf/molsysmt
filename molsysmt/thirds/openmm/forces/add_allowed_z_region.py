from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def add_allowed_z_region(molecular_system=None, selection='all', z0='0.0 nm', width='1.0 nm',
                         force_constant='5000 kilojoules_per_mole/nm**2', pbc=False, return_force=False,
                         syntax='MolSysMT', skip_digestion=False):

    from molsysmt import select, get, get_form
    from openmm import CustomExternalForce

    if molecular_system is not None:
        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    else:
        atom_indices = selection

    force_constant = puw.convert(force_constant, to_form='openmm.unit')
    z0 = puw.convert(z0, to_form='openmm.unit')
    width = puw.convert(width, to_form='openmm.unit')

    if pbc:
        potential = '0.5*Ka*q^2; q = max(0, d-wa); d = periodicdistance(0, 0, z, 0, 0, za)'
    else:
        potential = '0.5*Ka*q^2; q = max(0, d-wa); d = abs(z-za)'


    force = CustomExternalForce(potential)
    force.addGlobalParameter('Ka', force_constant)
    force.addGlobalParameter('wa', width/2.0)
    force.addGlobalParameter('za', z0)


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

