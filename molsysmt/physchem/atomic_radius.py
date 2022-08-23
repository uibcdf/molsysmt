from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def atomic_radius(molecular_system, selection='all', definition='vdw'):

    from molsysmt.basic import get
    from molsysmt.physico_chemical_properties.atoms.radius import units
    from molsysmt._private._digestion import digest_element

    if definition=='vdw':
        from molsysmt.physico_chemical_properties.atoms.radius import vdw as values
    else:
        raise NotImplementedError()


    atom_types = get(molecular_system, element='atom', selection=selection, type=True)

    output = []

    for ii in atom_types:
        var_aux = values[ii.capitalize()]
        output.append(var_aux)

    output = puw.quantity(np.array(output), units)

    return output

