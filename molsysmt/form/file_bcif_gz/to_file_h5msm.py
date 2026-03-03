from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:bcif.gz')
def to_file_h5msm(item, atom_indices='all', structure_indices='all', output_filename=None,
                  compression='gzip', compression_opts=4, int_precision='single', float_precision='single',
                  skip_digestion=False):

    from ..molsysmt_MolSys.to_molsysmt_MolSys import to_molsysmt_MolSys
    from ..molsysmt_MolSys.to_file_h5msm import to_file_h5msm as molsysmt_MolSys_to_file_h5msm

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                  structure_indices=structure_indices, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_file_h5msm(tmp_item, output_filename=output_filename, compression='gzip',
                                             compression_opts=4, int_precision='single', float_precision='single',
                                             skip_digestion=True)

    return tmp_item

