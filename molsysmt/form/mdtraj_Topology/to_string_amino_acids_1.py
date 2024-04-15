from molsysmt._private.digestion import digest

@digest(form='mdtraj.Topology')
def to_string_amino_acids_1(item, atom_indices='all', skip_digestion=False):

    from . import to_string_amino_acids_3
    from ..string_amino_acids_3 import to_string_amino_acids_1 as string_amino_acids_3_to_string_amino_acids_1

    tmp_item = to_string_amino_acids_3(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = string_amino_acids_3_to_string_amino_acids_1(tmp_item, skip_digestion=True)

    return tmp_item

