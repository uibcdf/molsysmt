from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'fasta': form_name
    }

def to_biopython_SeqRecord(item):
    from Bio.SeqIO import read as _Bio_SeqRecord_reader
    tmp_item=_Bio_SeqRecord_reader(item,'fasta')
    del(_Bio_SeqRecord_reader)
    return tmp_item
