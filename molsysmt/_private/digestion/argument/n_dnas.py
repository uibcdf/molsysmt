from molsysmt._private.exceptions import ArgumentError

def digest_n_dnas(n_dnas, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_dnas, bool):
            return n_dnas

    raise ArgumentError('n_dnas', value=n_dnas, caller=caller, message=None)

