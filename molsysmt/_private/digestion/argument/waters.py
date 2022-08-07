from molsysmt._private.exceptions import ArgumentError

def digest_waters(waters, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(waters, (bool, int)):
            return waters

    raise ArgumentError('waters', value=waters, caller=caller, message=None)

