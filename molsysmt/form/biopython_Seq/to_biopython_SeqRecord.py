from .is_biopython_Seq import is_biopython_Seq
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.atom_indices import digest_atom_indices

def to_biopython_SeqRecord(item, atom_indices='all', structure_indices='all',
                           id=None, name=None, description=None, check=True):

    if check:

        try:
            is_biopython_Seq(item)
        except:
            raise WrongFormError('biopython.Seq')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from Bio.SeqRecord import SeqRecord as Bio_SeqRecord
    from .extract import extract

    if id is None:
        id = 'None'
    if name is None:
        name = 'None'
    if description is None:
        description = 'None'

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)
    tmp_item = Bio_SeqRecord(tmp_item, id=id, name=name, description=description)

    return tmp_item

