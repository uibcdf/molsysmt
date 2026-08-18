from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def to_biopython_SeqRecord(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to biopython.SeqRecord.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.SeqRecord
        Converted molecular system representation.
    """

    from molsysmt.form.string_aminoacids1.to_string_aminoacids1 import to_string_aminoacids1
    from molsysmt.form.string_aminoacids1.to_biopython_SeqRecord import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    tmp_item = to_string_amionacids1(item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)
    tmp_item = string_aminoacids1_to_biopython_SeqRecord(tmp_item, skip_digestion=True)

    return tmp_item

