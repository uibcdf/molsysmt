from ...exceptions import ArgumentError

def digest_as_entity_2(as_entity_2, caller=None):

    from .as_entity import digest_as_entity

    try:
        return digest_as_entity(as_entity_2, caller=caller)
    except:
        raise ArgumentError('as_entity_2', value=as_entity_2, caller=caller, message=None)

