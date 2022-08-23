from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def mass(molecular_system, element ='atom', selection = 'all', syntax = 'MolSysMT'):

    from molsysmt.basic import get
    from molsysmt.physico_chemical_properties.atoms.mass import physical, units
    from molsysmt._private._digestion import digest_element

    element = digest_element(element)

    values=physical

    output = []
    if element == 'atom':
        atom_types = get(molecular_system, element=element, selection=selection, syntax=syntax, atom_type=True)
        for ii in atom_types:
            output.append(values[ii.capitalize()])
    elif element in ['group', 'component', 'molecule', 'chain', 'entity']:
        atom_types_in_element = get(molecular_system, element=element, selection=selection,
                                    syntax=syntaxi, atom_type=True)
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

    return output

