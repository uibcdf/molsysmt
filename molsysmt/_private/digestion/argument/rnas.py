from molsysmt._private.exceptions import ArgumentError

def digest_rnas(rnas, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(rnas, (bool, int)):
            return rnas

    raise ArgumentError('rnas', value=rnas, caller=caller, message=None)

