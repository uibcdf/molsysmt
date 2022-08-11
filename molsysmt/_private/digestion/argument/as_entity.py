from ...exceptions import ArgumentError

def digest_as_entity(as_entity, caller=None):

    if isinstance(as_entity, bool):
        return as_entity

    raise ArgumentError('as_entity', value=as_entity, caller=caller, message=None)

