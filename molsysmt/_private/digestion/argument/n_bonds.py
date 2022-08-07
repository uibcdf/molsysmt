from molsysmt._private.exceptions import ArgumentError

def digest_n_bonds(n_bonds, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_bonds, bool):
            return n_bonds

    raise ArgumentError('n_bonds', value=n_bonds, caller=caller, message=None)

