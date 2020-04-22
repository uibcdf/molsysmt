from os.path import basename as _basename
from Bio.Seq import Seq as _Bio_Seq

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _Bio_Seq : form_name,
    'biopython.Seq' : form_name,
    'Biopython.Seq' : form_name,
    'Bio.Seq' : form_name
}

info=["",""]

def to_biopython_SeqRecord(item, id=None, name=None, description=None, atom_indices='all', frame_indices='all'):

    from Bio.SeqRecord import SeqRecord as Bio_SeqRecord
    from .api_biopython_SeqRecord import extract_subsystem as extract_biopython_SeqRecord

    if id is None:
        id = 'None'
    if name is None:
        name = 'None'
    if description is None:
        description = 'None'

    tmp_item=Bio_SeqRecord(item, id=id, name=name, description=description)
    tmp_item=extract_biopython_SeqRecord(tmp_item, selection=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_fasta(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from molsysmt import extract as _extract
    from .api_biopython_SeqRecord import _to_fasta as _Bio_SeqRecord_to_fasta

    tmp_item=to_biopython_SeqRecord(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return _Bio_SeqRecord_to_fasta(tmp_item, output_file_path=output_file_path)

def duplicate(item):

    raise NotImplementedError

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

