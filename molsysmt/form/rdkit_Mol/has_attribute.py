from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='rdkit.Mol')
def has_attribute(item, attribute, skip_digestion=False):

    from .attributes import attributes
    return attributes.get(attribute, False)
