from molsysmt._private.exceptions import ArgumentError

def digest_n_bonds(n_bonds, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_bonds, bool):
            return n_bonds
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_bonds, (bool, int)):
            return n_bonds
    elif caller=='molsysmt.native.topology.__init__':
        if isinstance(n_bonds, int):
            return n_bonds

    raise ArgumentError('n_entities', value=n_entities, caller=caller, message=None)
