from molsysmt._private.exceptions import ArgumentError

def digest_n_components(n_components, caller=None):

    if caller=='get':
        if isinstance(n_components, bool):
            return n_components
        else:
            raise ArgumentError('n_components', caller=caller, message=None)
    else:
        raise ArgumentError('n_components', caller=caller, message=None)

