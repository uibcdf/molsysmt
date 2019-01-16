from os.path import basename as _basename
from Bio.SeqRecord import SeqRecord as _Bio_SeqRecord

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _Bio_SeqRecord : form_name,
    'biopython.SeqRecord' : form_name,
    'Biopython.SeqRecord' : form_name,
    'Bio.SeqRecord' : form_name
}

def to_fasta(item,output_file):
    from Bio.SeqIO import write as _Bio_SeqIO_write
    _Bio_SeqIO_write([item], output_file, 'fasta')
    pass

