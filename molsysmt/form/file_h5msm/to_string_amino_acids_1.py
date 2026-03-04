from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:h5msm')
def to_string_amino_acids_1(item, group_indices='all', skip_digestion=False):

    from .to_string_amino_acids_3 import to_string_amino_acids_3
    from molsysmt.form.string_amino_acids_3.to_string_amino_acids_1 import to_string_amino_acids_1 as string_amino_acids_3_to_string_amino_acids_1

    tmp_item = to_string_amino_acids_3(item, group_indices=group_indices)
    tmp_item = string_amino_acids_3_to_string_amino_acids_1(tmp_item)

    return tmp_item

