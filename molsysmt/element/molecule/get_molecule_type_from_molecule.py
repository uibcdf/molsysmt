from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def get_molecule_type_from_molecule(molecular_system, indices='all', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        indices = digest_indices(indices)

    from molsysmt.basic import get
    from . import get_molecule_type_from_group_names

    group_names_from_molecule = get(molecular_system, element='molecule', indices=indices, group_name=True)

    output = []

    for group_names in group_names_from_molecule:
        molecule_type = get_molecule_type_from_group_names(group_names)
        output.append(molecule_type)

    output = np.array(output, dtype=object)

    return output

