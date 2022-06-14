from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_biopython_SeqRecord(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'mdtraj.Trajectory')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_string_aminoacids1
    from ..string_aminoacids1 import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    tmp_item = to_string_amionacids1(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)
    tmp_item = string_aminoacids1_to_biopython_SeqRecord(tmp_item, check=False)

    return tmp_item

