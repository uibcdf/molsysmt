from molsysmt._private.exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )


def digest_n_groups(n_groups, caller=None):

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(n_groups, bool):
                return n_groups
            else:
                raise ArgumentError('n_groups', value=n_groups, caller=caller, message=None)
        elif caller=='molsysmt.basic.contains.contains':
            if isinstance(n_groups, (bool, int)):
                return n_groups
        elif caller=='molsysmt.basic.is_composed_of.is_composed_of':
            if isinstance(n_groups, (bool, int)):
                return n_groups

    raise ArgumentError('n_groups', value=n_groups, caller=caller, message=None)

