from molsysmt._private.exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )


def digest_n_molecules(n_molecules, caller=None):

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(n_molecules, bool):
                return n_molecules
            else:
                raise ArgumentError('n_molecules', value=n_molecules, caller=caller, message=None)
        elif caller=='molsysmt.basic.contains.contains':
            if isinstance(n_molecules, (bool, int)):
                return n_molecules

    raise ArgumentError('n_molecules', value=n_molecules, caller=caller, message=None)

