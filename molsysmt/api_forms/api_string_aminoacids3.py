# Corresponde al formato IUPAC extended protein que aparece en Biopython
def to_string_aminoacids1(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_aminoacids3 import to_string_aminoacids1 as string_aminoacids3_to_string_aminoacids1

    return string_aminoacids3_to_string_aminoacids1(item, atom_indices=atom_indices)


def to_biopython_Seq(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_aminoacids3 import to_biopython_Seq as string_aminoacids3_to_biopython_Seq

    return string_aminoacids3_to_biopython_Seq(item, atom_indices=atom_indices)


def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_aminoacids3 import to_biopython_SeqRecord as string_aminoacids3_to_biopython_SeqRecord

    return string_aminoacids3_to_biopython_SeqRecord(item, atom_indices=atom_indices)
