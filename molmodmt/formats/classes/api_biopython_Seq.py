from os.path import basename as _basename
from Bio.Seq import Seq as _Bio_Seq

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _Bio_Seq : form_name,
    'biopython.Seq' : form_name,
    'Biopython.Seq' : form_name,
    'Bio.Seq' : form_name
}

def to_biopython_SeqRecord(item):

    from Bio.SeqRecord import SeqRecord as _Bio_SeqRecord
    tmp_item=_Bio_SeqRecord(item)
    del(_Bio_SeqRecord)
    return tmp_item

def to_fasta(item, output_file):

    from .api_biopython_SeqRecord import _to_fasta as _Bio_SeqRecord_to_fasta
    tmp_item=to_biopython_SeqRecord(item)
    return _Bio_SeqRecord_to_fasta(tmp_item, output_file)

