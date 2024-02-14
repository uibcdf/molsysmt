from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def to_file_psf(item, atom_indices='all', output_filename=None):

    from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld as molsysmt_MolSysOld_to_molsysmt_TopologyOld
    from ..molsysmt_TopologyOld import to_file_psf as molsysmt_TopologyOld_to_file_psf

    tmp_item = molsysmt.MolSysOld_to_molsysmt_TopologyOld(item, atom_indices=atom_indices)
    tmp_item = molsysmt_TopologyOld_to_file_psf(tmp_item, output_filename=output_filename)

    return tmp_item

