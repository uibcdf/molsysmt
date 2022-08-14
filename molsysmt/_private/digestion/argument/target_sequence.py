from molsysmt._private.exceptions import ArgumentError

def digest_target_sequence(target_sequence, caller=None):

    if isinstance(target_sequence, str):
        return target_sequence

    raise ArgumentError('target_sequence', value=target_sequence, caller=caller, message=None)

