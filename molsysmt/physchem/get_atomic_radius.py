from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_atomic_radius(molecular_system, element='atom', selection='all', definition='vdw', syntax='MolSysMT',
                      skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.basic import get
    from molsysmt.physchem.atoms.radius import units

    if definition=='vdw':
        from molsysmt.physchem.atoms.radius import vdw as values
    else:
        raise NotImplementedError()


    atom_types = get(molecular_system, element='atom', selection=selection, atom_type=True)

    output = []

    for ii in atom_types:
        var_aux = values[ii.capitalize()]
        output.append(var_aux)

    output = puw.quantity(np.array(output), units)

    return output

