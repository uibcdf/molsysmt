from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology')
def to_string_amino_acids_1(item, group_indices='all', skip_digestion=False):

    from .to_string_amino_acids_3 import to_string_amino_acids_3
    from molsysmt.form.string_amino_acids_3 import to_string_amino_acids_1 as string_amino_acids_3_to_string_amino_acids_1

    tmp_item = to_string_amino_acids_3(item, group_indices=group_indices, skip_digestion=True)
    tmp_item = string_amino_acids_3_to_string_amino_acids_1(tmp_item, skip_digestion=True)

    return tmp_item
