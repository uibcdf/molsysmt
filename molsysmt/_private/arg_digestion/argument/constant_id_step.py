from ...exceptions import ArgumentError

def digest_constant_id_step(constant_id_step, caller=None):

    if isinstance(constant_id_step, bool):
        return constant_id_step

    raise ArgumentError('constant_id_step', value=constant_id_step, caller=caller, message=None)

