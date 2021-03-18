import numpy as np
from molsysmt import puw

def mass(molecular_system, target ='atom', selection = 'all'):

    from molsysmt.multitool import get
    from molsysmt.physico_chemical_properties.atoms.mass import physical, units
    from molsysmt._private_tools._digestion import digest_target

    target = digest_target(target)

    values=physical

    output = []
    if target == 'atom':
        atom_types = get(molecular_system, target=target, selection=selection, atom_type=True)
        for ii in atom_types:
            output.append(values[ii.capitalize()])
    elif target in ['group', 'component', 'molecule', 'chain', 'entity']:
        atom_types_in_target = get(molecular_system, target=target, selection=selection, atom_type=True)
        for aux in atom_types_in_target:
            output.append(np.sum([values[ii.capitalize()] for ii in aux]))
    elif target == 'system':
        atom_types_in_target = get(molecular_system, target='atom', selection='all', atom_type=True)
        output.append(np.sum([values[ii.capitalize()] for ii in atom_types_in_target]))

    if target =='system':
        output = output[0]*puw.unit(units)
    else:
        output = puw.quantity(np.array(output), units)

    return output

