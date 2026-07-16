from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='rdkit.Mol')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):

    from .attributes import attributes

    output = attributes.get(attribute, False)
    if output and not include_none and attribute == 'isotope':
        output = any(atom.GetIsotope() != 0 for atom in item.GetAtoms())
    return output
