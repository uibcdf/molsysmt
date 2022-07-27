from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_Topology(item, atom_indices='all'):

    if check:

        digest_item(item, 'openmm.Simulation')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_openmm_Topology as openmm_Simulation_to_openmm_Topology
    from molsysmt.item.openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = openmm_Simulation_to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

