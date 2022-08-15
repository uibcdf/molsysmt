from molsysmt._private.exceptions import ArgumentError

def digest_n_chains(n_chains, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_chains, bool):
            return n_chains

    raise ArgumentError('n_chains', values=n_chains, caller=caller, message=None)

