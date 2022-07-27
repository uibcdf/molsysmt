from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_Topology import is_molsysmt_Topology

def to_string_pdb_text(item, atom_indices='all', coordinates=None, box=None):

    if check:

        digest_item(item, 'molsysmt.Topology')
        atom_indices = digest_atom_indices(atom_indices)
        coordinates = digest_coordinates(coordinates)

    from . import to_openmm_Topology
    from ..openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    tmp_item =  to_openmm_Topology(item, box, atom_indices=atom_indices)
    tmp_item =  openmm_Topology_to_string_pdb_text(tmp_item, coordinates=coordinates)

    return tmp_item

