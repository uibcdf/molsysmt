from molsysmt._private.digestion import digest

@digest()
def get_molecule_type_from_group_names(group_names):

    from ..component import get_component_type_from_group_names

    return get_component_type_from_group_names(group_names)

