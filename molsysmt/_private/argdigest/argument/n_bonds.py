from molsysmt._private.smonitor import ArgumentError

def digest_n_bonds(n_bonds, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_bonds, bool):
            return n_bonds
    elif caller=='molsysmt.basic.compare.compare':
        if isinstance(n_bonds, bool):
            return n_bonds
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_bonds, (bool, int)):
            return n_bonds
    elif caller=='molsysmt.native.topology.__init__':
        if isinstance(n_bonds, int):
            return n_bonds
    elif caller=='molsysmt.native.molsys.__init__':
        if isinstance(n_bonds, int):
            return n_bonds

    raise ArgumentError('n_bonds', value=n_bonds, caller=caller, message=None)
