from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','')+':seq'

is_form={
    'aminoacids3:seq' : form_name,
    'aminoacids3' : form_name
}

info=["",""]

### Corresponde al formato IUPAC extended protein que aparece en Biopython

def to_aminoacids1_seq(item, atom_indices='all', frame_indices='all'):

    from Bio.SeqUtils import seq1
    tmp_item = seq1(item.replace('aminoacids3:',''))
    return 'aminoacids1:'+tmp_item

def to_biopython_Seq(item, atom_indices='all', frame_indices='all'):

    from .api_aminoacids1 import to_biopython_Seq as aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = _aminoacis1_to_biopython_Seq(tmp_item)
    return tmp_item

def to_biopython_SeqRecord(item, atom_indices='all', frame_indices='all'):

    from .api_aminoacids1 import to_biopython_SeqRecord as aminoacids1_to_biopython_SeqRecord
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacis1_to_biopython_SeqRecord(tmp_item)
    return tmp_item

def to_fasta(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from .api_aminoacids1 import to_fasta as aminoacids1_to_fasta
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return aminoacis1_to_fasta(tmp_item, output_file_path=output_file_path)

def select_with_MDTraj(item, selection):
    raise NotImplementedError

def extract_subsystem(item, atom_indices='all', frame_indices='all'):
    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError


###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

