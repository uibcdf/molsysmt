from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_mass(molecular_system, element ='atom', selection = 'all', syntax = 'MolSysMT', method='physical',
             skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.basic import get, get_form
    from molsysmt.physchem.atoms.mass import physical, units

    output = []

    if method=='physical':

        if element == 'atom':
            atom_types = get(molecular_system, element=element, selection=selection, syntax=syntax, atom_type=True)
            for ii in atom_types:
                output.append(physical[ii.capitalize()])
        elif element in ['group', 'component', 'molecule', 'chain', 'entity']:
            atom_types_in_element = get(molecular_system, element=element, selection=selection,
                                        syntax=syntax, atom_type=True)
            for aux in atom_types_in_element:
                output.append(np.sum([physical[ii.capitalize()] for ii in aux]))
        elif element == 'system':
            atom_types_in_element = get(molecular_system, element='atom', selection='all',
                                        syntax=syntax, atom_type=True)
            output.append(np.sum([physical[ii.capitalize()] for ii in atom_types_in_element]))

        if element =='system':
            output = output[0]*puw.unit(units)
        else:
            output = puw.quantity(np.array(output), units)
    
    elif method=='OpenMM':

        from openmm import unit as _unit

        form_in = get_form(molecular_system)

        if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

            if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
                from openmm.app import ForceField
                forcefield_openmm = _digest_forcefields(forcefield)
                system = ForceField(*forcefield_openmm).createSystem(item.topology)

            elif form_in == "openmm.System":
                system = item

            if element == 'atom':
                atom_indices = get(molecular_system, element=element, selection=selection, syntax=syntax, atom_indices=True)
                for ii in atom_indices:
                    output.append(system.getParticleMass(ii))
            elif element in ['group', 'component', 'molecule', 'chain', 'entity']:
                atom_indices_in_element = get(molecular_system, element=element, selection=selection,
                                            syntax=syntax, atom_indices=True)
                for aux in atom_types_in_element:
                    output.append(np.sum([system.getParticleMass(ii) for ii in aux]))
            elif element == 'system':
                if is_all(selection):
                    aux = 0.0 * _unit.amu
                    for ii in range(system.getNumParticles()):
                        aux += system.getParticleMass(ii)
                    output=aux
                else:
                    raise NotImplementedError

        else:
            raise NotImplementedError

    output = puw.standardize(output)

    return output

