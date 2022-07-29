from molsysmt._private.exceptions import ArgumentError

def digest_n_groups(n_groups, caller=None):

    if caller=='get':
        if isinstance(n_groups, bool):
            return n_groups
        else:
            raise ArgumentError('n_groups', caller=caller, message=None)
    else:
        raise ArgumentError('n_groups', caller=caller, message=None)

