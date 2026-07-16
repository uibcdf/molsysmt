"""Resolving form-independent attributes from declared source attributes."""

NOT_DERIVABLE = object()

DERIVED_ATTRIBUTE_DEPENDENCIES = {
    'box_shape': 'box',
    'box_angles': 'box',
    'box_lengths': 'box',
    'box_volume': 'box',
}


def can_derive_attribute(module, attribute_name, element):
    """Return whether a form can derive an attribute at the requested level."""
    if element != 'system':
        return False

    source_attribute = DERIVED_ATTRIBUTE_DEPENDENCIES.get(attribute_name)
    if source_attribute is None:
        return False

    from molsysmt.attribute import attributes

    if attributes[attribute_name]['depends_on'] != [source_attribute]:
        return False

    source_getter = getattr(module, f'get_{source_attribute}_from_system', None)
    return callable(source_getter) and module.attributes.get(source_attribute, False)


def derive_attribute(module, item, attribute_name, element, structure_indices='all'):
    """Derive an attribute or return ``NOT_DERIVABLE`` when no route exists."""
    if not can_derive_attribute(module, attribute_name, element):
        return NOT_DERIVABLE

    source_attribute = DERIVED_ATTRIBUTE_DEPENDENCIES[attribute_name]
    source_getter = getattr(module, f'get_{source_attribute}_from_system')
    source_value = source_getter(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    if source_value is None:
        return None

    if attribute_name == 'box_shape':
        from molsysmt.pbc import get_shape_from_box

        return get_shape_from_box(source_value, skip_digestion=True)
    if attribute_name == 'box_angles':
        from molsysmt.pbc import get_angles_from_box

        return get_angles_from_box(source_value, skip_digestion=True)
    if attribute_name == 'box_lengths':
        from molsysmt.pbc import get_lengths_from_box

        return get_lengths_from_box(source_value, skip_digestion=True)
    if attribute_name == 'box_volume':
        from molsysmt.pbc import get_volume_from_box

        return get_volume_from_box(source_value)

    return NOT_DERIVABLE
