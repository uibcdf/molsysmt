from os.path import basename as _basename
from os import remove as _remove

form_name=_basename(__file__).split('.')[0][4:]+':id'

is_form = {
    'uniprot:id': form_name,
    'UniProt:id': form_name
    }

def to_aminoacids1_seq(form_id):

    import urllib as _urllib

    url_fasta = 'http://www.uniprot.org/uniprot/'+UniProt_id+'.fasta'
    request_fasta = _urllib.request.Request(url_fasta)
    request_fasta.add_header('User-Agent', 'Python at https://github.com/uibcdf/MolModMT || prada.gracia@gmail.com')
    response_fasta = _urllib.request.urlopen(request_fasta)
    fasta_result = response_fasta.read().decode('utf-8')
    lines_fasta=fasta_result.split('\n')
    tmp_sequence=''.join(lines_fasta[1:])
    del(url_fasta,request_fasta,response_fasta,fasta_result)
    return tmp_sequence

def to_aminoacids3_seq(form_id):
    from molmodmt.formats.seqs.api_aminoacids1 import to_aminoacids3_seq as _to_aa3_seq
    tmp_sequence = to_aminoacids1_seq(form_id)
    tmp_sequence = _to_aa3_seq(tmp_sequence)
    del(_to_aa3_seq)
    return tmp_sequence

