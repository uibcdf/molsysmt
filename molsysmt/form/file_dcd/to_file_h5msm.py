from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:dcd')
def to_file_h5msm(item, atom_indices='all', structure_indices='all', output_filename=None,
        compression='gzip', compression_opts=4, int_precision='single', float_precision='single',
                  skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.to_file_h5msm import to_file_h5msm as molsysmt_Structures_to_file_h5msm

    tmp_item = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                      structure_indices=structure_indices, skip_digestion=True)
    return molsysmt_Structures_to_file_h5msm(tmp_item, output_filename=output_filename,
            compression=compression, compression_opts=compression_opts,
            int_precision=int_precision, float_precision=float_precision,
            skip_digestion=True)
