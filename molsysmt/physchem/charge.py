from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw

@digest()
def charge(molecular_system, element='group', selection='all', definition=None, engine='OpenMM',
        syntax='MolSysMT'):

    if definition in ['physical_pH7', 'collantes']:

        from molsysmt.basic import get

        if definition=='physical_pH7':
            from molsysmt.physchem.groups.charge import physical_pH7 as values, units
        elif definition=='collantes':
            from molsysmt.physchem.groups.charge import collantes as values, units
        else:
            raise NotImplementedMethodError()

        output = []

        if element=='atom':
            raise ValueError('Only elements bigger than, or equal to, groups are allowed when definition is "physical_pH7" or "collantes"')

        elif element=='group':

            group_names = get(molecular_system, element=element, selection=selection, group_name=True)
            for ii in group_names:
                output.append(values[ii.upper()])

        elif element in ['component', 'molecule', 'chain', 'entity']:

            group_names = get(molecular_system, element=element, selection=selection, group_name=True)
            for aux in group_names:
                output.append(np.sum([values[ii.upper()] for ii in aux]))

        elif element=='system':

            group_names = get(molecular_system, element='group', selection='all', group_names=True)
            output.append(np.sum([values[ii.upper()] for ii in group_names]))

        if element =='system':
            output = output[0]*puw.unit(units)
        else:
            output = puw.quantity(np.array(output), units)

    else:

        from molsysmt.basic import get, convert, get_form

        if engine == 'OpenMM':

            from openmm import NonbondedForce

            openmm_system = convert(molecular_system, to_form='openmm.System')

            output = []

            if element=='atom':

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            output.append(force.getParticleParameters(int(index))[0]._value)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif element in ['group', 'component', 'chain', 'molecule', 'entity']:

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for atom_list in atom_indices:
                            var_aux = 0.0
                            for index in atom_list:
                                var_aux+=force.getParticleParameters(int(index))[0]._value
                            output.append(var_aux)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif element=='system':

                atom_indices = get(molecular_system, element='atom', selection='all', index=True)

                var_aux = 0.0
                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            var_aux+=force.getParticleParameters(int(index))[0]._value

                output = np.round(var_aux,4)*puw.unit('e')

        else:

            raise NotImplementedMethodError

    return output

