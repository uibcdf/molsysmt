from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_file_pdb(item, coordinates, box, atom_indices='all', output_filename=None, digest=True):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, box, atom_indices=atom_indices, digest=False)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates, output_filename=output_filename, digest=False)

    return tmp_item

