import numpy as np
from molsysmt import puw
from molsysmt._private_tools.exceptions import *

def charge(molecular_system, target='group', selection='all', type=None, engine='OpenMM'):

    from molsysmt._private_tools._digestion import digest_engine, digest_target

    engine=digest_engine(engine)
    target=digest_target(target)

    if type in ['physical_pH7', 'collantes']:

        from molsysmt.basic import get

        from molsysmt.physico_chemical_properties.groups.charge import units
        if type=='physical_pH7':
            from molsysmt.physico_chemical_properties.groups.charge import physical_pH7 as values, units
        elif type=='collantes':
            from molsysmt.physico_chemical_properties.groups.charge import collantes as values, units
        else:
            raise NotImplementedError()

        output = []

        if target=='atom':
            raise ValueError('Only targets bigger than, or equal to, groups are allowed when type is "physical_pH7" or "collantes"')

        elif target=='group':

            group_names = get(molecular_system, target = target, selection = selection, group_name = True)
            for ii in group_names:
                output.append(values[ii.upper()])

        elif target in ['component', 'molecule', 'chain', 'entity']:

            group_names = get(molecular_system, target = target, selection = selection, group_name = True)
            for aux in group_names:
                output.append(np.sum([values[ii.upper()] for ii in aux]))

        elif target=='system':

            group_names = get(molecular_system, target = 'group', selection = 'all', group_names = True)
            output.append(np.sum([values[ii.upper()] for ii in group_names]))

        if target =='system':
            output = output[0]*puw.unit(units)
        else:
            output = puw.quantity(np.array(output), units)

    else:

        from molsysmt._private_tools._digestion import digest_molecular_system
        from molsysmt.basic import get, convert, get_form

        molecular_system = digest_molecular_system(molecular_system)

        if engine == 'OpenMM':

            from simtk.openmm import NonbondedForce

            openmm_system = convert(molecular_system, to_form='openmm.System')

            output = []

            if target=='atom':

                atom_indices = get(molecular_system, target = target, selection = selection, atom_index = True)

                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            output.append(force.getParticleParameters(int(index))[0]._value)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif target in ['group', 'component', 'chain', 'molecule', 'entity']:

                atom_indices = get(molecular_system, target = target, selection = selection, atom_index = True)

                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for atom_list in atom_indices:
                            var_aux = 0.0
                            for index in atom_list:
                                var_aux+=force.getParticleParameters(int(index))[0]._value
                            output.append(var_aux)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif target=='system':

                atom_indices = get(molecular_system, target = 'atom', selection = 'all', index = True)

                var_aux = 0.0
                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            var_aux+=force.getParticleParameters(int(index))[0]._value

                output = np.round(var_aux,4)*puw.unit('e')

        else:

            raise NotImplementedError

    return output

