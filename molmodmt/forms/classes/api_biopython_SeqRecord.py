from os.path import basename as _basename
from Bio.SeqRecord import SeqRecord as _Bio_SeqRecord

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _Bio_SeqRecord : form_name,
    'biopython.SeqRecord' : form_name,
    'Biopython.SeqRecord' : form_name,
    'Bio.SeqRecord' : form_name
}

def to_fasta(item, output_file_path=None, atom_indices=None, frame_indices=None):

    from Bio.SeqIO import write as Bio_SeqIO_write

    tmp_item = extract_subsystem(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return Bio_SeqIO_write([tmp_item], filename, 'fasta')

def to_pir(item, output_file_path=None, style=None, atom_indices=None, frame_indices=None):

    from Bio.SeqIO.PirIO import PirWriter as _PirWriter
    from molmodmt.forms.files.api_pir import rewrite_to_style as _rewrite

    tmp_item = extract_subsystem(item, atom_indices=atom_indices, frame_indices=frame_indices)

    handle = open(filename,"w")
    writer = _PirWriter(handle)
    writer.write_file(item)
    handle.close()
    return _rewrite(filename=filename, style=style)

def extract_subsystem(item, atom_indices=None, frame_indices=None):

    if (atom_indices is None) and (frame_indices is None):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

