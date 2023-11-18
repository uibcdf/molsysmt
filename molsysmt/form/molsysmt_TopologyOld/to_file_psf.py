from molsysmt._private.digestion import digest

@digest(form='molsysmt.TopologyOld')
def to_file_psf(item, atom_indices='all', output_filename=None):

    from .to_openmm_Topology import to_openmm_Topology as molsysmt_TopologyOld_to_openmm_Topology
    from ..openmm_Topology import to_file_psf as openmm_Topology_to_file_psf

    tmp_item = molsysmt_TopologyOld_to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_file_psf(tmp_item, output_filename=output_filename)

    return tmp_item

