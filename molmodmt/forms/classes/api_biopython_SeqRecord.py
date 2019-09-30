from os.path import basename as _basename
from Bio.SeqRecord import SeqRecord as _Bio_SeqRecord

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _Bio_SeqRecord : form_name,
    'biopython.SeqRecord' : form_name,
    'Biopython.SeqRecord' : form_name,
    'Bio.SeqRecord' : form_name
}

def to_fasta(item, filename=None, atom_indices=None, frame_indices=None):
    from Bio.SeqIO import write as _Bio_SeqIO_write
    _Bio_SeqIO_write([item], filename, 'fasta')
    pass

def to_pir(item, filename=None, style=None, atom_indices=None, frame_indices=None):
    from Bio.SeqIO.PirIO import PirWriter as _PirWriter
    from molmodmt.forms.files.api_pir import rewrite_to_style as _rewrite

    print(item)

    handle = open(filename,"w")
    writer = _PirWriter(handle)
    writer.write_file(item)
    handle.close()
    _rewrite(filename=filename, style=style)
    pass
