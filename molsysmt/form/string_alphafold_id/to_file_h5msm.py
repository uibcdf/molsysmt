from molsysmt._private.digestion import digest

@digest(form='string:alphafold_id')
def to_file_h5msm(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_file_h5msm as molsysmt_MolSys_to_file_h5msm

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_file_h5msm(tmp_item, output_filename=output_filename, skip_digestion=True)

    return tmp_item

