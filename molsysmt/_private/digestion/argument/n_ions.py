from molsysmt._private.exceptions import ArgumentError

def digest_n_ions(n_ions, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_ions, bool):
            return n_ions

    raise ArgumentError('n_ions', value=n_ions, caller=caller, message=None)

