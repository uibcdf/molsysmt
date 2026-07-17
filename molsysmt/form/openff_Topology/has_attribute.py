from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openff.Topology')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):

    from .attributes import attributes
    if attribute == 'partial_charge':
        molecules = list(item.molecules)
        return bool(molecules) and all(
            molecule.partial_charges is not None for molecule in molecules
        )
    return attributes.get(attribute, False)
