from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def add_allowed_plane_region(molecular_system=None, selection='all',
                             force_constant='5000 kilojoules_per_mole/nm**2', point='[0,0,0] nm',
                             normal_vector=[0,0,1], width='1.0 nm', pbc=False, return_force=False,
                             syntax='MolSysMT', skip_digestion=False):

    from molsysmt import select, get, get_form
    from openmm import CustomExternalForce
    from openmm import unit as u

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    force_constant = puw.convert(force_constant, to_form='openmm.unit')
    point = puw.convert(point, to_form='openmm.unit')[0]
    width = puw.convert(width, to_form='openmm.unit')

    if np.allclose(normal_vector, [1.0, 0.0, 0.0]):

        if pbc:
            potential = '0.5*Ka*q^2; q = max(0, d-wa); d = periodicdistance(x, 0, 0, px, 0, 0)'
        else:
            potential = '0.5*Ka*q^2; q = max(0, d-wa); d = abs(x-px)'

        force = CustomExternalForce(potential)
        force.addGlobalParameter('Ka', force_constant)
        force.addGlobalParameter('wa', width/2.0)
        force.addGlobalParameter('px', point[0])

    elif np.allclose(normal_vector, [0.0, 1.0 , 0.0]):

        if pbc:
            potential = '0.5*Ka*q^2; q = max(0, d-wa); d = periodicdistance(0, y, 0, 0, py, 0)'
        else:
            potential = '0.5*Ka*q^2; q = max(0, d-wa); d = abs(y-py)'

        force = CustomExternalForce(potential)
        force.addGlobalParameter('Ka', force_constant)
        force.addGlobalParameter('wa', width/2.0)
        force.addGlobalParameter('py', point[1])

    elif np.allclose(normal_vector, [0.0, 0.0, 1.0]):

        if pbc:
            potential = '0.5*Ka*q^2; q = max(0, d-wa); d = periodicdistance(0, 0, z, 0, 0, pz)'
        else:
            potential = '0.5*Ka*q^2; q = max(0, d-wa); d = abs(z-pz)'

        force = CustomExternalForce(potential)
        force.addGlobalParameter('Ka', force_constant)
        force.addGlobalParameter('wa', width/2.0)
        force.addGlobalParameter('pz', point[2])

    else:

        if pbc:
            potential = (
                '0.5*Ka*q^2; '
                'q = max(0, d-wa); '
                'd = abs(periodicdistance(a, b, c, 0, 0, 0)); '
                'a = u*vx; '
                'b = u*vy; '
                'c = u*vz; '
                'u = (x-px)*vx+(y-py)*vy+(z-pz)*vz;'
            )
        else:
            potential = (
                '0.5*Ka*q^2; '
                'q = max(0, d-wa); '
                'd = abs((x-px)*vx+(y-py)*vy+(z-pz)*vz);'
            )

        force = CustomExternalForce(potential)
        force.addGlobalParameter('Ka', force_constant)
        force.addGlobalParameter('wa', width/2.0)
        force.addGlobalParameter('px', point[0])
        force.addGlobalParameter('py', point[1])
        force.addGlobalParameter('pz', point[2])
        force.addGlobalParameter('vx', normal_vector[0])
        force.addGlobalParameter('vy', normal_vector[1])
        force.addGlobalParameter('vz', normal_vector[2])

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

