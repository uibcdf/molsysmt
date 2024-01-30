from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_file_pdb(item, atom_indices='all', coordinates=None, output_filename=None, skip_digestion=False):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates=coordinates, output_filename=output_filename,
                                           skip_digestion=True)

    return tmp_item

