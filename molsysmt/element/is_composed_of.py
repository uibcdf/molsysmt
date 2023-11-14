def is_composed_of(element_1, element_2):

    from molsysmt.element import _element_plural_to_singular
    from molsysmt.element import _element_singular_to_plural

    if element_1 in _element_plural_to_singular:
        element_1 = _element_plural_to_singular[element_1]

    if element_2 in _element_plural_to_singular:
        element_2 = _element_plural_to_singular[element_2]

    if element_1 == 'system':
        if element_2 in ['atom', 'group', 'component', 'molecule', 'entity', 'bond', 'chain']:
            return True

    elif element_1 == 'chain':
        if element_2 in ['atom', 'group', 'component', 'molecule', 'entity']:
            return True

    elif element_1 == 'entity':
        if element_2 in ['atom', 'group', 'component', 'molecule']:
            return True

    elif element_1 == 'molecule':
        if element_2 in ['atom', 'group', 'component']:
            return True

    elif element_1 == 'component':
        if element_2 in ['atom', 'group']:
            return True

    elif element_1 == 'group':
        if element_2 == 'atom':
            return True

    return False

