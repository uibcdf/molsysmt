from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def get_mass(molecular_system, element ='system', selection = 'all', syntax = 'MolSysMT', definition='physical',
             skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.basic import get, get_form
    from molsysmt.physchem.atoms.mass import physical, units

    output = []

    if definition=='physical':

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
    
    elif definition=='OpenMM':

        from openmm import unit as _unit

        form_in = get_form(molecular_system)

        if form_in in ["openmm.Modeller", "openmm.Topology", "pdbfixer.PDBFixer"]:

            if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
                openmm_topology = molecular_system.Topology
            else:
                openmm_topology = molecular_system

            openmm_atoms = list(openmm_topology.atoms())

            if element == 'atom':
                atom_indices = get(openmm_topology, element=element, selection=selection, syntax=syntax, atom_indices=True)
                for ii in atom_indices:
                    output.append(openmm_atoms[ii].element.mass)
                output = puw.utils.sequences.concatenate(output)
            elif element in ['group', 'component', 'molecule', 'chain', 'entity']:
                atom_indices_in_element = get(openmm_topology, element=element, selection=selection,
                                            syntax=syntax, atom_indices=True)
                for aux in atom_indices_in_element:
                    output.append(np.sum([openmm_atoms[ii].element.mass for ii in aux]))
                output = puw.utils.sequences.concatenate(output)
            elif element == 'system':
                if is_all(selection):
                    aux = 0.0*_unit.amu
                    for ii in openmm_atoms:
                        aux += ii.element.mass
                    output=aux
                else:
                    raise NotImplementedError

        elif form_in == "openmm.System":

            if element == 'atom':
                atom_indices = get(molecular_system, element=element, selection=selection, syntax=syntax, atom_indices=True)
                for ii in atom_indices:
                    output.append(molecular_system.getParticleMass(ii))
                output = puw.utils.sequences.concatenate(output)
            elif element == 'system':
                if is_all(selection):
                    aux = 0.0 * _unit.amu
                    for ii in range(molecular_system.getNumParticles()):
                        aux += molecular_system.getParticleMass(ii)
                    output=aux
                else:
                    raise NotImplementedError
            else:
                raise NotImplementedError

        else:
            raise NotImplementedError

    output = puw.standardize(output)

    return output

