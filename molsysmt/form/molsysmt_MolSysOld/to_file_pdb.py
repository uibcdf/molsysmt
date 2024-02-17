from molsysmt._private.digestion import *

@digest(form='molsysmt.MolSysOld')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom
    from ..openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, atom_indices=atom_indices,
            coordinates=coordinates, output_filename=output_filename, skip_digestion=True)

    return tmp_item

