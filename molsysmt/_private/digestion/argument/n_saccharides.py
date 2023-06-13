from molsysmt._private.exceptions import ArgumentError

def digest_n_saccharides(n_saccharides, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_saccharides, bool):
            return n_saccharides
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_saccharides, (bool, int)):
            return n_saccharides

    raise ArgumentError('n_saccharides', value=n_saccharides, caller=caller, message=None)

