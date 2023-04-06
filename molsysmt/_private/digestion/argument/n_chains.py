from molsysmt._private.exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )


def digest_n_chains(n_chains, caller=None):

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(n_chains, bool):
                return n_chains
            else:
                raise ArgumentError('n_chains', value=n_chains, caller=caller, message=None)

    raise ArgumentError('n_chains', value=n_chains, caller=caller, message=None)

