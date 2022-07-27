from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'openmm.Modeller')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_openmm_Topology
    from ..openmm_Topology import to_mdtraj_Topology as openmm_Topology_to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item,  atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = openmm_Topology_to_mdtraj_Topology(tmp_item)

    return tmp_item

