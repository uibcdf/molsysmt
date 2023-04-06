from molsysmt._private.exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )


def digest_n_entities(n_entities, caller=None):

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(n_entities, bool):
                return n_entities
            else:
                raise ArgumentError('n_entities', value=n_entities, caller=caller, message=None)

    raise ArgumentError('n_entities', value=n_entities, caller=caller, message=None)

