from .is_openmm_Modeller import is_openmm_Modeller
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_Topology(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'openmm.Modeller')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from ..openmm_Topology import extract as extract_openmm_Topology

    tmp_item = item.getTopology()
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

