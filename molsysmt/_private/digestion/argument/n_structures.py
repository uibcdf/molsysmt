from molsysmt._private.exceptions import ArgumentError

def digest_n_structures(n_structures, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_structures, bool):
            return n_structures

    raise ArgumentError('n_structures', value=n_structures, caller=caller, message=None)

