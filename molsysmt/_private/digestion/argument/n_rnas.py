from molsysmt._private.exceptions import ArgumentError

def digest_n_rnas(n_rnas, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_rnas, bool):
            return n_rnas

    raise ArgumentError('n_rnas', value=n_rnas, caller=caller, message=None)

