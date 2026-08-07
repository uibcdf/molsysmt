from molsysmt._private.smonitor import ArgumentError
import numpy as np

def digest_step(step, caller=None):

    if isinstance(step, int):
        return step

    raise ArgumentError('step', value=step, caller=caller, message=None)

