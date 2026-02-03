from molsysmt._private.exceptions import ArgumentError

_anion_values = [
    'Cl-', 'Br-', 'F-', 'I-'
]

def digest_anion(anion, caller=None):

    if isinstance(anion, str):
        if anion in _anion_values:
            return anion

    raise ArgumentError('anion', value=anion, caller=caller, message=None)

