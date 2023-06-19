from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_label(molecular_system,
              element='atom',
              selection='all',
              string='{atom_name}-{atom_id}@{atom_index}',
              syntax='MolSysMT',
         ):

    from . import get
    from molsysmt.attribute import attributes as _attributes

    get_attributes = {}
    for attribute in _attributes.keys():
        if attribute in string:
            get_attributes[attribute] = True

    get_dict = get(molecular_system, element=element, selection=selection, syntax=syntax,
                       output_type='dictionary', **get_attributes)

    n_elements = []
    for value in get_dict.values():
        n_elements.append(len(value))


    output = []

    if np.all(np.array(n_elements)==n_elements[0]):

        aux_dict = {key:'' for key in get_dict.keys()}

        for ii in range(n_elements[0]):
            for key in get_dict.keys():
                aux_dict[key]=get_dict[key][ii]
            output.append(string.format(**aux_dict))

    if len(output)>1:
        return output
    else:
        return output[0]

