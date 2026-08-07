from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):

    from .attributes import attributes
    if attribute == 'partial_charge':
        return item.partial_charges is not None
    if attribute in {'coordinates', 'structure_id', 'structure_index'}:
        return item.n_conformers > 0
    return attributes.get(attribute, False)
