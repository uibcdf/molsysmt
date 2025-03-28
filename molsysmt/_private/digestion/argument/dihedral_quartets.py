from ...exceptions import ArgumentError
import numpy as np

def digest_dihedral_quartets(dihedral_quartets, caller=None):

    from .quartets import digest_quartets

    try:
        return digest_quartets(dihedral_quartets, caller=caller)
    except:
        raise ArgumentError('dihedral_quartets', value=dihedral_quartets, caller=caller, message=None)

