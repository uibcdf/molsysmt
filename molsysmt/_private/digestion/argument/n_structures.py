from molsysmt._private.exceptions import ArgumentError

def digest_n_structures(n_structures, caller=None):

    if caller=='get':
        if isinstance(n_structures, bool):
            return n_structures
        else:
            raise ArgumentError('n_structures', caller=caller, message=None)
    else:
        raise ArgumentError('n_structures', caller=caller, message=None)

