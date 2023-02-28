# Corresponde al formato IUPAC extended protein que aparece en Biopython
def to_string_aminoacids3(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_aminoacids1 import to_string_aminoacids3 as string_aminoacids1_to_string_aminoacids3

    return string_aminoacids1_to_string_aminoacids3(item)


def to_biopython_Seq(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    return string_aminoacids1_to_biopython_Seq(item)


def to_biopython_SeqRecord(item, molecular_system=None, atom_indices='all', structure_indices='all', id=None, name=None,
                           description=None):
    from molsysmt.form.string_aminoacids1 import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    return string_aminoacids1_to_biopython_SeqRecord(item)
