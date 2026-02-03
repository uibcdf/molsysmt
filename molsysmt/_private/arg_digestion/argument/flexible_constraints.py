from molsysmt._private.exceptions import ArgumentError

def digest_flexible_constraints(flexible_constraints, caller=None):


    if caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return flexible_constraints
    elif isinstance(flexible_constraints, str):
        return flexible_constraints

    raise ArgumentError('flexible_constraints', value=flexible_constraints, caller=caller, message=None)

