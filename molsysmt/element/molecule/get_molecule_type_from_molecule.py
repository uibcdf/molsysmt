from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_molecule_type_from_molecule(molecular_system, indices='all', digest=True):

    from molsysmt.basic import get
    from . import get_molecule_type_from_group_names

    group_names_from_molecule = get(molecular_system, element='molecule', indices=indices, group_name=True, digest=False)

    output = []

    for group_names in group_names_from_molecule:
        molecule_type = get_molecule_type_from_group_names(group_names, digest=False)
        output.append(molecule_type)

    output = np.array(output, dtype=object)

    return output

