from molsysmt._private.smonitor import ArgumentError

def digest_constraints(constraints, caller=None):


    if caller is not None and caller.startswith('molsysmt.form.') and '.to_' in caller:
        return constraints
    elif isinstance(constraints, str):
        return constraints

    raise ArgumentError('constraints', value=constraints, caller=caller, message=None)

