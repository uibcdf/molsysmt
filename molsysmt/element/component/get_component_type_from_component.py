from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_component_type_from_component(molecular_system, indices='all'):

    from molsysmt.basic import get
    from . import get_component_type_from_group_names

    group_names_from_component = get(molecular_system, element='component', indices=indices, group_name=True)

    output = []

    for group_names in group_types_from_component:
        component_type = get_component_type_from_group_names(group_names)
        output.append(component_type)

    output = np.array(output, dtype=object)

    return output

