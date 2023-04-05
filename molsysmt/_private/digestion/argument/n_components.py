from molsysmt._private.exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )


def digest_n_components(n_components, caller=None):

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(n_components, bool):
                return n_components
            else:
                raise ArgumentError('n_components', value=n_components, caller=caller, message=None)

    raise ArgumentError('n_components', value=n_components, caller=caller, message=None)

