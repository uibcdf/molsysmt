from molsysmt._private.exceptions import ArgumentError
from molsysmt._private.variables import is_all
import numpy as np

_methods_1 = [
        'molsysmt.topology.get_dihedral_quartets.get_dihedral_quartets',
        'molsysmt.structure.get_dihedral_angles.get_dihedral_angles',
        ]
_dihedral_angles_1 = ['phi', 'psi', 'omega', 'chi1', 'chi2', 'chi3', 'chi4', 'chi5',
        'phi-psi', 'phi-psi-omega']

def digest_dihedral_angle(dihedral_angle, caller=None):

    if dihedral_angle is None:
        return None

    if is_all(dihedral_angle):
        return 'all'

    if isinstance(dihedral_angle, str):
        if caller in _methods_1:
            if dihedral_angle.lower() in _dihedral_angles_1:
                return dihedral_angle.lower()

    raise ArgumentError('dihedral_angle', value=dihedral_angle, caller=caller, message=None)
