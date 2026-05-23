from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='biopython.PDBStructure')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from .attributes import attributes

    output = attributes.get(attribute, False)

    return output
