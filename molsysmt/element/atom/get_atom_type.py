from molsysmt._private.digestion import digest
from .names import atom as atom_type_from_name
import numpy as np


@digest()
def get_atom_type(molecular_system, element='atom', selection='all', redefine_types=False, syntax='MolSysMT'):

    raise NotImplementedError

