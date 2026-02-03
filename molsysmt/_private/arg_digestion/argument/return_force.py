from ...exceptions import ArgumentError

def digest_return_force(return_force, caller=None):

    if isinstance(return_force, bool):
        return return_force

    raise ArgumentError('return_force', value=return_force, caller=caller, message=None)

