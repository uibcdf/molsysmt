from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='molsysmt.MolSys')
@dep_digest('Bio')
def to_biopython_SeqRecord(item, atom_indices='all', skip_digestion=False):

    from .to_string_amino_acids_1 import to_string_amino_acids_1
    from molsysmt.form.string_amino_acids_1.to_biopython_SeqRecord import to_biopython_SeqRecord as string_amino_acids_1_to_biopython_SeqRecord
    from . import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    tmp_item = to_string_amino_acids_1(item, group_indices=group_indices, skip_digestion=True)
    tmp_item = string_amino_acids_1_to_biopython_SeqRecord(tmp_item, skip_digestion=True)

    return tmp_item
