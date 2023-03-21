from molsysmt._private.exceptions import ArgumentError

def digest_constraints(constraints, caller=None):


    if caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return constraints
    elif isinstance(constraints, str):
        return constraints

    raise ArgumentError('constraints', value=constraints, caller=caller, message=None)

