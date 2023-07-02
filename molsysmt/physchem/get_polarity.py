from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_polarity(molecular_system, selection = 'all', syntax='MolSysMT', definition='grantham'):
    """
    To be written soon...
    """

    from molsysmt.basic import get

    if definition == 'grantham':
        from molsysmt.physico_chemical_properties.groups.polarity import grantham as values
    elif definition == 'zimmerman':
        from molsysmt.physico_chemical_properties.groups.polarity import zimmerman as values
    else:
        raise NotImplementedMethodError()

    group_names = get(molecular_system, element='group', selection=selection, syntax=syntax, group_name=True)

    output = []

    for ii in group_names:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

