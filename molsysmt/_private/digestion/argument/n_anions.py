from molsysmt._private.exceptions import ArgumentError

def digest_n_anions(n_anions, caller=None):

    if caller=='molsysmt.build.solvate.solvate':
        if isinstance(n_anions, str):
            if n_anions == 'neutralize':
                return 'neutralize'
        if isinstance(n_anions, int):
            return n_anions

    raise ArgumentError('n_anions', value=n_anions, caller=caller, message=None)

