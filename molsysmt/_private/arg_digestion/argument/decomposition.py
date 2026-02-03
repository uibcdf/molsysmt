from molsysmt._private.exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.molecular_mechanics.get_potential_energy.get_potential_energy',
        )

def digest_decomposition(decomposition, caller=None):

    if caller.endswith(functions_with_boolean):
        if isinstance(decomposition, bool):
            return decomposition

    if isinstance(decomposition, str):
        from molsysmt.attribute import attributes
        if decomposition in attributes['decomposition']['values']:
            return decomposition

    raise ArgumentError('decomposition', value=decomposition, caller=caller, message=None)

