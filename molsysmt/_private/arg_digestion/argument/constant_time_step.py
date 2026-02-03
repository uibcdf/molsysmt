from ...exceptions import ArgumentError

def digest_constant_time_step(constant_time_step, caller=None):

    if isinstance(constant_time_step, bool):
        return constant_time_step

    raise ArgumentError('constant_time_step', value=constant_time_step, caller=caller, message=None)

