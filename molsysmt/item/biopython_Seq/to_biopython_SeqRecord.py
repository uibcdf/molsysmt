from molsysmt._private.digestion import digest

@digest(form='biopython.Seq')
def to_biopython_SeqRecord(item, atom_indices='all',
                           id=None, name=None, description=None):

    from Bio.SeqRecord import SeqRecord as Bio_SeqRecord
    from .extract import extract

    if id is None:
        id = 'None'
    if name is None:
        name = 'None'
    if description is None:
        description = 'None'

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False)
    tmp_item = Bio_SeqRecord(tmp_item, id=id, name=name, description=description)

    return tmp_item

