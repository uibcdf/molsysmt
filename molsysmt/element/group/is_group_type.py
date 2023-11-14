def is_group_type(group_type):

    from molsysmt.element.group import _group_types
    from molsysmt.element.group import _plural_group_types_to_singular

    output = False

    if group_type in _group_types:
        output = True

    elif group_type in _plural_group_types_to_singular:
        output = True

    return output

