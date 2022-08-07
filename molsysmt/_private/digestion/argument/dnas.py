from molsysmt._private.exceptions import ArgumentError

def digest_dnas(dnas, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(dnas, (bool, int)):
            return dnas

    raise ArgumentError('dnas', value=dnas, caller=caller, message=None)

