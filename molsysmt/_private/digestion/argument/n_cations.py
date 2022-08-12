from molsysmt._private.exceptions import ArgumentError

def digest_n_cations(n_cations, caller=None):

    if caller=='molsysmt.build.solvate.solvate':
        if isinstance(n_cations, str):
            if n_cations == 'neutralize':
                return 'neutralize'
        if isinstance(n_cations, int):
            return n_cations

    raise ArgumentError('n_cations', value=n_cations, caller=caller, message=None)

