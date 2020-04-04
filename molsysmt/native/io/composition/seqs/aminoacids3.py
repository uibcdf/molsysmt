def to_aminoacids3_seq(item, indices='all', frame_indices='all'):

    from molsysmt.native.io.composition.classes.molsysmt_DataFrame import to_molsysmt_DataFrame
    from molsysmt.native.io.dataframe.seqs.aminoacids3 import to_aminoacids3 as molsysmt_DataFrame_to_aminoacids3

    tmp_item=to_molsysmt_DataFrame(item, indices=indices, frame_indices=frame_indices)
    tmp_item=molsysmt_DataFrame_to_aminoacids3(item)

    return tmp_item

