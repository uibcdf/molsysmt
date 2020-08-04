import numpy as np

def get_charge(item, target='atom', selection = 'all', type='Phys_pH7', forcefield=None, engine='OpenMM'):

    from molsysmt import get
    from simtk import unit

    output = []

    if type in ['Phys_pH7', 'Collantes']:

        if type=='Phys_pH7':
            from .residues.charge import phys_ph7 as residues_charge
        elif type=='Collantes':
            from .residues.charge import collantes as residues_charge

        if target=='atom':
            raise ValueError('Only target="group" is allowed when type=="phys_ph7"')

        elif target=='group':

            residue_names = get(item, target = 'group', selection = selection, name = True)

            for ii in residue_names:
                var_aux = residues_charge[ii]
                output.append(var_aux)

            output = np.array(output, dtype=float)*unit.elementary_charge

        elif target in ['component', 'molecule', 'chain', 'entity']:

            residue_names = get(item, target = target, selection = selection, group_name = True)

            for list_residues in residue_names:
                var_aux = 0.0
                for ii in list_residues:
                    var_aux += residues_charge[ii]
                output.append(var_aux)

            output = np.array(output, dtype=float)*unit.elementary_charge

        elif target=='system':

            residue_names = get(item, target = 'group', selection = 'all', group_name = True)

            var_aux = 0.0
            for ii in residue_names:
                var_aux += residues_charge[ii]

            output = var_aux*unit.elementary_charge

    elif type=='ForceField':

        from molsysmt.utils.engines import digest as _digest_engines
        from molsysmt.utils.forcefields import digest as _digest_forcefields

        engine = _digest_engines(engine)

        if engine == 'OpenMM':

            if forcefield is not None:

                forcefields = _digest_forcefields(forcefield, engine=engine)
                from molsysmt import convert
                from simtk.openmm.app import ForceField
                from simtk.openmm import NonbondedForce

                topology = convert(item, to_form='openmm.Topology')
                system = ForceField(*forcefields).createSystem(topology)

            else:

                from molsysmt import get_form
                if get_form(item)!='openmm.System':
                    raise ValueError('The item is not an openmm.System object. A value for the \
input argument forcefield is needed if engine=="OpenMM"')
                else:
                    system=item

            if target=='atom':

                atom_indices = get(item, target = target, selection = selection, index = True)

                for force_index in range(system.getNumForces()):
                    force = system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            output.append(force.getParticleParameters(int(index))[0]._value)

                output = np.array(output, dtype=float)*unit.elementary_charge

            elif target in ['group', 'component', 'chain', 'molecule', 'entity']:

                atom_indices = get(item, target = target, selection = selection, atom_index = True)

                for force_index in range(system.getNumForces()):
                    force = system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for atom_list in atom_indices:
                            var_aux = 0.0
                            for index in atom_list:
                                var_aux+=force.getParticleParameters(int(index))[0]._value
                            output.append(var_aux)

                output = np.array(output, dtype=float)*unit.elementary_charge

            elif target=='system':

                atom_indices = get(item, target = 'atom', selection = 'all', index = True)

                var_aux = 0.0
                for force_index in range(system.getNumForces()):
                    force = system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            var_aux+=force.getParticleParameters(int(index))[0]._value

                output = int(round(var_aux))*unit.elementary_charge

    else:
        raise NotImplementedError

    return output

def get_masses(item, target ='atom', selection = 'all'):
    
    from .atoms.weight import weight as atomic_weight 
    from molsysmt import get
    from simtk import unit

    atom_types = get(item, target = 'atom', selection = selection, type = True)

    output = []

    for ii in atom_types:
        var_aux = atomic_weight[ii]
        output.append(var_aux*unit.amu)

    return output

def get_radii(item, target = 'atom', selection = 'all', radius_type = 'vdw'):

    from .atoms.vdw_radius import vdw as vdw_radius 
    from molsysmt import get
    from simtk import unit

    atom_types = get(item, target = 'atom', selection = selection, type = True)

    output = []

    for ii in atom_types:
        var_aux = vdw_radius[ii]
        output.append(var_aux*unit.picometers)

    return output

def get_polarity(item, target = 'group', selection = 'all', polarity_type = 'grantham'):

    from molsysmt import get
    from simtk import unit

    residue_types = get(item, target = 'residue', selection = selection, name = True)

    output = []

    if polarity_type == 'grantham':

        from .residues.polarity import grantham as polarity

    elif polarity_type == 'zimmerman':

        from .residues.polarity import zimmerman as polarity

    for ii in residue_types:
        var_aux = polarity[ii]
        output.append(var_aux)


    return output

def get_transmembrane_tendency(item, target = 'group', selection = 'all',
                               transmembrane_tendency_type = 'zhao'):

    from molsysmt import get
    from simtk import unit

    residue_types = get(item, target = 'residue', selection = selection, name = True)

    output = []

    if transmembrane_tendency_type == 'zhao':

        from .residues.transmembrane_tendency import zhao as transmembrane_tendency

    elif transmembrane_tendency_type == 'senes':

        from .residues.transmembrane_tendency import senes as transmembrane_tendency

    for ii in residue_types:
        var_aux = transmembrane_tendency[ii]
        output.append(var_aux)

    return output


