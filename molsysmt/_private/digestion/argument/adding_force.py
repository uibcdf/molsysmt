from ...exceptions import ArgumentError

def digest_adding_force(adding_force, caller=None):

    if isinstance(adding_force, bool):
        return adding_force

    raise ArgumentError('adding_force', value=adding_force, caller=caller, message=None)

