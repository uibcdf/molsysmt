def to_aminoacids1_seq (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids3 import to_aminoacids1_seq as aminoacids3_seq_to_aminoacids1_seq
    from .aminoacids3 import to_aminoacids3_seq as molsysmt_Topology_to_aminoacids3_seq
    tmp_item = molsysmt_Topology_to_aminoacids3_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids3_seq_to_aminoacids1_seq(tmp_item)

    return tmp_item
