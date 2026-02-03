from molsysmt._private.exceptions import ArgumentError

_cation_values = [
    'Cs+', 'K+', 'Li+', 'Na+', 'Rb+',
]

def digest_cation(cation, caller=None):

    if isinstance(cation, str):
        if cation in _cation_values:
            return cation

    raise ArgumentError('cation', value=cation, caller=caller, message=None)

