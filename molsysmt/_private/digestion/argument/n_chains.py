from molsysmt._private.exceptions import ArgumentError

def digest_n_chains(n_chains, caller=None):

    if caller=='get':
        if isinstance(n_chains, bool):
            return n_chains
        else:
            raise ArgumentError('n_chains', caller=caller, message=None)
    else:
        raise ArgumentError('n_chains', caller=caller, message=None)

