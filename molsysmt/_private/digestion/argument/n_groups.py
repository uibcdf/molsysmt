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

    raise ArgumentError('n_groups', value=n_groups, caller=caller, message=None)

