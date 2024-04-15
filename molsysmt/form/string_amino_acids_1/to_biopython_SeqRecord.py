from molsysmt._private.digestion import digest

@digest(form='string:amino_acids_1')
def to_biopython_SeqRecord(item, group_indices='all', skip_digestion=False):

    from . import to_biopython_Seq
    from ..biopython_Seq import to_biopython_SeqRecord as biopython_Seq_to_biopython_SeqRecord

    tmp_item = to_biopython_Seq(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                skip_digestion=True)
    tmp_item = biopython_Seq_to_biopython_SeqRecord(tmp_item, skip_digestion=True)

    return tmp_item

