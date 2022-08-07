from molsysmt._private.exceptions import ArgumentError

def digest_n_lipids(n_lipids, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_lipids, bool):
            return n_lipids

    raise ArgumentError('n_lipids', value=n_lipids, caller=caller, message=None)

