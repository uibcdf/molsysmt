from molsysmt._private.exceptions import ArgumentError

def digest_n_components(n_components, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_components, bool):
            return n_components

    raise ArgumentError('n_components', values=n_components, caller=caller, message=None)

