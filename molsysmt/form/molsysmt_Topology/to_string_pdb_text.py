from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_Topology import is_molsysmt_Topology

def to_string_pdb_text(item, atom_indices='all', coordinates=None, box=None, check=True):

    if check:

        digest_item(item, 'molsysmt.Topology')
        atom_indices = digest_atom_indices(atom_indices)
        coordinates = digest_coordinates(coordinates)

    from . import to_openmm_Topology
    from ..openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    tmp_item =  to_openmm_Topology(item, box, atom_indices=atom_indices, check=False)
    tmp_item =  openmm_Topology_to_string_pdb_text(tmp_item, coordinates=coordinates, check=False)

    return tmp_item

