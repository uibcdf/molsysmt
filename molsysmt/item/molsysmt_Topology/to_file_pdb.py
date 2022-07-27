from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_file_pdb(item, coordinates, box, atom_indices='all', output_filename=None):

    if check:

        digest_item(item, 'molsysmt.Topology')
        atom_indices = digest_atom_indices(atom_indices)
        coordinates = digest_coordinates(coordinates)
        box = digest_box(box)

    if output_filename is None:
        raise ValueError

    from . import to_openmm_Topology
    from ..openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, box, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates, output_filename=output_filename)

    return tmp_item

