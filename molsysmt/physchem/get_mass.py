from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_mass(molecular_system, element ='atom', selection = 'all', syntax = 'MolSysMT', method='physical',
             forcefield=['AMBER99SB-ILDN','TIP3P'], to_form='dict', skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.basic import get, get_form
    from molsysmt.physchem.atoms.mass import physical, units

    if method=='physical':

        values=physical

        output = []
        if element == 'atom':
            atom_types = get(molecular_system, element=element, selection=selection, syntax=syntax, atom_type=True)
            for ii in atom_types:
                output.append(values[ii.capitalize()])
        elif element in ['group', 'component', 'molecule', 'chain', 'entity']:
            atom_types_in_element = get(molecular_system, element=element, selection=selection,
                                        syntax=syntax, atom_type=True)
            for aux in atom_types_in_element:
                output.append(np.sum([values[ii.capitalize()] for ii in aux]))
        elif element == 'system':
            atom_types_in_element = get(molecular_system, element='atom', selection='all',
                                        syntax=syntax, atom_type=True)
            output.append(np.sum([values[ii.capitalize()] for ii in atom_types_in_element]))

        if element =='system':
            output = output[0]*puw.unit(units)
        else:
            output = puw.quantity(np.array(output), units)
    
    elif method=='OpenMM':

        mass_per_atom=[]

        form_in = get_form(molecular_system)

        if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

            if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
                from openmm.app import ForceField
                forcefield_openmm = _digest_forcefields(forcefield)
                system = ForceField(*forcefield_openmm).createSystem(item.topology)

            elif form_in == "openmm.System":
                system = item

            atom_indices = set(atom_indices)
            for particle_index in range(system.getNumParticles()):
                if particle_index in atom_indices:
                    mass.append(system.getParticleMass(particle_index))
            return mass

        else:
            raise NotImplementedError


    return output

