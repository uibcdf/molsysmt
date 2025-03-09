from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw

@digest()
def get_charge(molecular_system, element='group', selection='all', definition='physical_pH7',
               forcefield='AMBER14', water_model=None, syntax='MolSysMT', skip_digestion=False):
    """
    To be written soon...
    """
    
    from molsysmt.basic import get

    if definition in ['physical_pH7', 'collantes']:


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
            output = puw.quantity(np.array(output), units)

        elif element in ['component', 'molecule', 'chain', 'entity']:

            group_names = get(molecular_system, element=element, selection=selection, group_name=True)
            for aux in group_names:
                output.append(np.sum([values[ii.upper()] for ii in aux]))
            output = puw.quantity(np.array(output), units)

        elif element=='system':

            group_names = get(molecular_system, element='group', selection='all', group_names=True)
            output = puw.quantity(np.sum([values[ii.upper()] for ii in group_names]), units)

    elif definition == 'OpenMM':

        from molsysmt.basic import convert, get_form
        from openmm import NonbondedForce

        form_in = get_form(molecular_system)

        if form_in == 'openmm.System':

            if element=='atom':

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                output = []

                for force_index in range(molecular_system.getNumForces()):
                    force = molecular_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            output.append(force.getParticleParameters(int(index))[0]._value)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif element in ['group', 'component', 'chain', 'molecule', 'entity']:

                raise ValueError('openmm.System only allows element in ["atom", "system"]')

            elif element=='system':

                var_aux = 0.0
                for force_index in range(molecular_system.getNumForces()):
                    force = molecular_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in range(molecular_system.getNumParticles()):
                            var_aux+=force.getParticleParameters(int(index))[0]._value

                output = np.round(var_aux,4)*puw.unit('e')

        elif form_in == 'openmm.Simulation':

            if element=='atom':

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                output = []

                for force_index in range(molecular_system.system.getNumForces()):
                    force = molecular_system.system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            output.append(force.getParticleParameters(int(index))[0]._value)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif element in ['group', 'component', 'chain', 'molecule', 'entity']:

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                output = []

                for force_index in range(molecular_system.system.getNumForces()):
                    force = molecular_system.system.getForce(force_index)
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
                for force_index in range(molecular_system.system.getNumForces()):
                    force = molecular_system.system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            var_aux+=force.getParticleParameters(int(index))[0]._value

                output = np.round(var_aux,4)*puw.unit('e')

        else:

            openmm_system = convert(molecular_system, to_form='openmm.System', forcefield=forcefield)

            if element=='atom':

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                output = []

                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            output.append(force.getParticleParameters(int(index))[0]._value)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif element in ['group', 'component', 'chain', 'molecule', 'entity']:

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                output = []

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

                var_aux = 0.0
                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in range(openmm_system.getNumParticles()):
                            var_aux+=force.getParticleParameters(int(index))[0]._value

                output = np.round(var_aux,4)*puw.unit('e')

    else:

        raise NotImplementedMethodError

    output = puw.standardize(output)

    return output

