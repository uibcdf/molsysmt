from molsysmt._private.argdigest import arg_digest

@arg_digest(form='rdkit.Mol')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):

    from .attributes import attributes

    output = attributes.get(attribute, False)
    if output and not include_none:
        if attribute == 'isotope':
            output = any(atom.GetIsotope() != 0 for atom in item.GetAtoms())
        elif attribute == 'partial_charge':
            from .get_mechanical_attributes import _get_partial_charges

            output = _get_partial_charges(item) is not None
        elif attribute in {'coordinates', 'structure_id'}:
            output = item.GetNumConformers() > 0
    return output
