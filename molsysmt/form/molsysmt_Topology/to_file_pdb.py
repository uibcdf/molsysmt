from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology')
def to_file_pdb(item, coordinates, box, atom_indices='all', output_filename=None, skip_digestion=False):

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_file_pdb import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, box, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates, output_filename=output_filename)

    return tmp_item

