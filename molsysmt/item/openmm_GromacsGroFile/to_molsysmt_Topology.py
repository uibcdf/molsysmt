from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'openmm.GromacsGroFile')
        atom_indices = digest_atom_indices(atom_indices)

    from . import to_openmm_Topology
    from ..api_openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = to_openmm_Topology(item, check=check)
    tmp_item = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, check=check)

    return tmp_item

