from molsysmt._private.exceptions import ArgumentError

def digest_n_entities(n_entities, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_entities, bool):
            return n_entities

    raise ArgumentError('n_entities', values=n_entities, caller=caller, message=None)

