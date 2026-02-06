from molsysmt.exceptions import ArgumentError
import numpy as np

def digest_string(string, caller=None):

    if isinstance(string, str):
        return string

    raise ArgumentError('string', value=string, caller=caller, message=None)

