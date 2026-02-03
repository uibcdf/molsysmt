from ...exceptions import ArgumentError

def digest_id_step(id_step, caller=None):

    if id_step is None:
        return None

    if isinstance(id_step, int):
        return id_step

    raise ArgumentError('id_step', value=id_step, caller=caller, message=None)

