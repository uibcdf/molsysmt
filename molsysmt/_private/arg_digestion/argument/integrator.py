from molsysmt._private.exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )

def digest_integrator(integrator, caller=None):

    if caller.endswith(functions_with_boolean):
        if isinstance(integrator, bool):
            return integrator

    if isinstance(integrator, str):
        from molsysmt.attribute import attributes
        if integrator in attributes['integrator']['values']:
            return integrator

    raise ArgumentError('integrator', value=integrator, caller=caller, message=None)

