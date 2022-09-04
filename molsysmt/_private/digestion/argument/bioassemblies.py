import numpy as np
from ...exceptions import ArgumentError

def digest_bioassemblies(bioassemblies, caller=None):

    if caller=='molsysmt.basic.get.get':

        if isinstance(bioassemblies, bool):
            return bioassemblies

    raise ArgumentError('bioassemblies', value=bioassemblies, caller=caller, message=None)
