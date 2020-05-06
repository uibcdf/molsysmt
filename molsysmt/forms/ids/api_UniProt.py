from os.path import basename as _basename
from os import remove as _remove

form_name=_basename(__file__).split('.')[0][4:]+':id'

is_form = {
    'uniprot:id': form_name,
    'UniProt:id': form_name
    }

info=["",""]
with_topology=True
with_trajectory=False

def to_aminoacids1_seq(item, atom_indices='all', frame_indices='all'):

    import urllib as _urllib

    url_fasta = 'http://www.uniprot.org/uniprot/'+UniProt_id+'.fasta'
    request_fasta = _urllib.request.Request(url_fasta)
    request_fasta.add_header('User-Agent', 'Python at https://github.com/uibcdf/MolSysMT || prada.gracia@gmail.com')
    response_fasta = _urllib.request.urlopen(request_fasta)
    fasta_result = response_fasta.read().decode('utf-8')
    lines_fasta=fasta_result.split('\n')
    tmp_sequence=''.join(lines_fasta[1:])
    del(url_fasta,request_fasta,response_fasta,fasta_result)
    return tmp_sequence

def to_aminoacids3_seq(item, atom_indices='all', frame_indices='all'):
    from molsysmt.forms.seqs.api_aminoacids1 import to_aminoacids3_seq as _to_aa3_seq
    tmp_sequence = to_aminoacids1_seq(item)
    tmp_sequence = _to_aa3_seq(tmp_sequence)
    del(_to_aa3_seq)
    return tmp_sequence

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

