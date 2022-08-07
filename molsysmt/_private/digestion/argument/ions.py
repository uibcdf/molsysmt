from molsysmt._private.exceptions import ArgumentError

def digest_ions(ions, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(ions, (bool, int)):
            return ions

    raise ArgumentError('ions', value=ions, caller=caller, message=None)

