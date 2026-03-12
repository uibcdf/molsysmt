from molsysmt._private.smonitor import ArgumentError

def digest_flexible_constraints(flexible_constraints, caller=None):

    if caller is not None and caller.startswith('molsysmt.form.') and '.to_' in caller:
        return flexible_constraints
    elif isinstance(flexible_constraints, str):
        return flexible_constraints

    raise ArgumentError('flexible_constraints', value=flexible_constraints, caller=caller, message=None)

