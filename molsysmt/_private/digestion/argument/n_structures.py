from molsysmt._private.exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )

def digest_n_structures(n_structures, caller=None):

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(n_structures, bool):
                return n_structures
            else:
                raise ArgumentError('n_structures', value=n_structures, caller=caller, message=None)
        elif caller=='molsysmt.basic.contains.contains':
            if isinstance(n_molecules, (bool, int)):
                return n_molecules

    raise ArgumentError('n_structures', value=n_structures, caller=caller, message=None)

