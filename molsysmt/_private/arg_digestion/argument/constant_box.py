from ...exceptions import ArgumentError

def digest_constant_box(constant_box, caller=None):

    if isinstance(constant_box, bool):
        return constant_box

    raise ArgumentError('constant_box', value=constant_box, caller=caller, message=None)

