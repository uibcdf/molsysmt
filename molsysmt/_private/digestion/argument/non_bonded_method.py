from molsysmt._private.exceptions import ArgumentError

def digest_non_bonded_method(non_bonded_method, caller=None):

    if isinstance(non_bonded_method, str):
        return non_bonded_method

    raise ArgumentError('non_bonded_method', value=non_bonded_method, caller=caller, message=None)

