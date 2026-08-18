def is_composed_of(element_1, element_2):
    """
    Checking whether a molecular system or subset is composed of specific element types.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity'}, default='group'
        Target element level to evaluate.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection of elements to inspect.
    syntax : str, default='MolSysMT'
        Selection syntax used.
    skip_digestion : bool, default=False
        Whether to skip argument validation.
    **kwargs : dict
        Keyword arguments specifying expected element types (e.g. `amino_acids=True`, `water=False`).

    Returns
    -------
    bool
        True if composition criteria match, False otherwise.

    .. versionadded:: 1.0.0
    """

    from molsysmt.element import _plural_elements_to_singular

    if element_1 in _plural_elements_to_singular:
        element_1 = _plural_elements_to_singular[element_1]

    if element_2 in _plural_elements_to_singular:
        element_2 = _plural_elements_to_singular[element_2]

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
