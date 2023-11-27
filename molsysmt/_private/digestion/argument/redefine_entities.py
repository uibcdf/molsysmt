from ...exceptions import ArgumentError

def digest_redefine_entities(redefine_entities, caller=None):

    if isinstance(redefine_entities, bool):
        return redefine_entities

    raise ArgumentError('redefine_entities', value=redefine_entities, caller=caller, message=None)

