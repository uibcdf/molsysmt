from molsysmt._private.exceptions import ArgumentError

def digest_attribute(attribute, caller=None):

    from molsysmt.attribute import is_attribute

    if is_attribute(attribute):
        return attribute
    else:
        raise ArgumentError('attribute', value=attribute, caller=caller, message=None)

