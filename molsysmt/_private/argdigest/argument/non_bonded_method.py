from molsysmt._private.smonitor import ArgumentError

def digest_non_bonded_method(non_bonded_method, caller=None):

    if caller is not None and caller.startswith('molsysmt.form.') and '.to_' in caller:
        return non_bonded_method
    elif isinstance(non_bonded_method, str):
        return non_bonded_method

    raise ArgumentError('non_bonded_method', value=non_bonded_method, caller=caller, message=None)

