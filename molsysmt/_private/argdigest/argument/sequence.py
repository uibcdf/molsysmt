from molsysmt._private.smonitor import ArgumentError
from ...variables import is_all

def digest_sequence(sequence, caller=None):

    if sequence is None:
        return None

    if isinstance(sequence, str):
        return sequence

    if isinstance(sequence, dict):
        return sequence

    raise ArgumentError('sequence', value=sequence, caller=caller, message=None)
