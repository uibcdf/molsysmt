from molsysmt._private.smonitor import ArgumentError

def digest_n_inner_bonds(n_inner_bonds, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_inner_bonds, bool):
            return n_inner_bonds
    elif caller=='molsysmt.basic.compare.compare':
        if isinstance(n_inner_bonds, bool):
            return n_inner_bonds

    raise ArgumentError('n_inner_bonds', value=n_inner_bonds, caller=caller, message=None)
