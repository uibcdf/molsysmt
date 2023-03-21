from molsysmt._private.exceptions import ArgumentError

def digest_attribute(attribute, caller=None):

    from molsysmt.attribute import is_attribute

    if is_attribute(attribute.lower()):
        return attribute.lower()
    elif caller == 'molsysmt.basic.has_attribute.has_attribute':
        if attribute.lower() in ['structural', 'topological', 'mechanical']:
            return attribute.lower()

    raise ArgumentError('attribute', value=attribute, caller=caller, message=None)

