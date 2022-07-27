from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'openmm.Simulation')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_openmm_Context as openmm_Simulation_to_openmm_Context
    from molsysmt.item.openmm_Context import to_molsysmt_Structures as openmm_Context_to_molsysmt_Structures

    tmp_item = openmm_Simulation_to_openmm_Context(item)
    tmp_item = openmm_Context_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

