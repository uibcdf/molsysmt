def to_aminoacids1_seq (item, atom_indices='all', frame_indices='all'):

    from molsysmt import convert
    from .aminoacids3 import to_aminoacids3_seq
    tmp_item = to_aminoacids3_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = convert(tmp_item, to_form="aminoacids1:seq")

    return tmp_item
