from molsysmt._private.exceptions import ArgumentError

def digest_n_aminoacids(n_aminoacids, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_aminoacids, bool):
            return n_aminoacids

    raise ArgumentError('n_aminoacids', value=n_aminoacids, caller=caller, message=None)

