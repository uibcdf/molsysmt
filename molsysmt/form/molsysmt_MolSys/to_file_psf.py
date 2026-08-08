from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_file_psf(item, atom_indices='all', output_filename=None, skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology.to_file_psf import to_file_psf as molsysmt_Topology_to_file_psf

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(
        item, atom_indices=atom_indices, skip_digestion=True
    )
    tmp_item = molsysmt_Topology_to_file_psf(tmp_item, output_filename=output_filename, skip_digestion=True)

    return tmp_item
