from molsysmt._private.exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )


def digest_n_chains(n_chains, caller=None):

    if caller.endswith(functions_with_boolean):
        if isinstance(n_chains, bool):
            return n_chains
        else:
            raise ArgumentError('n_chains', value=n_chains, caller=caller, message=None)
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_chains, (bool, int)):
            return n_chains
    elif caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(n_chains, (bool, int)):
            return n_chains
    elif caller=='molsysmt.native.topology.__init__':
        if isinstance(n_chains, int):
            return n_chains
    elif caller=='molsysmt.native.molsys.__init__':
        if isinstance(n_chains, int):
            return n_chains

    raise ArgumentError('n_chains', value=n_chains, caller=caller, message=None)

