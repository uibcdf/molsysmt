from molsysmt._private.digestion import digest
from .names import atom as atom_type_from_name
import numpy as np


@digest()
def get_atom_type(molecular_system, element='atom', selection='all', redefine_types=False, syntax='MolSysMT'):

    raise NotImplementedError



def _get_atom_type_from_atom_name(atom_name):
    """
    To be written soon...
    """

    try:
        return atom_type_from_name[atom_name]
    except:
        print(atom_name)
        return 'ANK'

