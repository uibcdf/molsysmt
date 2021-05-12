def to_aminoacids1_seq (item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids3_seq import to_aminoacids1_seq as aminoacids3_seq_to_aminoacids1_seq
    from .aminoacids3_seq import to_aminoacids3_seq as molsysmt_Topology_to_aminoacids3_seq

    tmp_item, tmp_molecular_system = molsysmt_Topology_to_aminoacids3_seq(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = aminoacids3_seq_to_aminoacids1_seq(tmp_item, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

