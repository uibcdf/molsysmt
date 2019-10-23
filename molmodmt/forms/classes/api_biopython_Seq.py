from os.path import basename as _basename
from Bio.Seq import Seq as _Bio_Seq

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _Bio_Seq : form_name,
    'biopython.Seq' : form_name,
    'Biopython.Seq' : form_name,
    'Bio.Seq' : form_name
}

def to_biopython_SeqRecord(item, id=None, name=None, description=None, atom_indices=None,
                           frame_indices=None):

    from molmodmt import extract as _extract
    from Bio.SeqRecord import SeqRecord as _Bio_SeqRecord

    if id is None:
        id = 'None'
    if name is None:
        name = 'None'
    if description is None:
        description = 'None'

    tmp_item=_Bio_SeqRecord(item, id=id, name=name, description=description)
    tmp_item=_extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)
    del(_Bio_SeqRecord)
    return tmp_item

def to_fasta(item, output_file, atom_indices=None, frame_indices=None):
    from molmodmt import extract as _extract
    from .api_biopython_SeqRecord import _to_fasta as _Bio_SeqRecord_to_fasta
    tmp_item=to_biopython_SeqRecord(item)
    tmp_item=_extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)
    return _Bio_SeqRecord_to_fasta(tmp_item, output_file)

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

