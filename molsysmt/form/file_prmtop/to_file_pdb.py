from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_file_pdb(item, atom_indices='all', coordinates=None, output_filename=None):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates=coordinates, output_filename=output_filename)

    return tmp_item

def _to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None):

    return to_file_pdb(item, atom_indices=atom_indices, output_filename=output_filename)

