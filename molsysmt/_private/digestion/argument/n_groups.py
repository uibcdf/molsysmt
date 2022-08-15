from molsysmt._private.exceptions import ArgumentError

def digest_n_groups(n_groups, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_groups, bool):
            return n_groups

    raise ArgumentError('n_groups', values=n_groups, caller=caller, message=None)

