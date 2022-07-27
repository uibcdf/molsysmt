from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_Context(item, atom_indices='all', coordinates=None):

    if check:

        digest_item(item, 'openmm.Topology')
        atom_indices = digest_atom_indices(atom_indices)
        coordinates = digest_coordinates(coordinates)

    from . import to_openmm_System
    from ..openmm_System import to_openmm_Context as openmm_System_to_openmm_Context

    tmp_item = to_openmm_System(item, atom_indices=atom_indices, coordinates=coordinates)
    tmp_item = openmm_System_to_openmm_Context(tmp_item)

    return tmp_item

