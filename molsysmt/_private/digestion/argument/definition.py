import numpy as np
from ...exceptions import ArgumentError

def digest_definition(definition, caller=None):

    if isinstance(definition, str):
        return definition

    return ArgumentError('definition', value=definition, caller=caller, message=None)

