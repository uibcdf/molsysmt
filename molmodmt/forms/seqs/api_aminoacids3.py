from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','')+':seq'

is_form={
    'aminoacids3:seq' : form_name,
    'aminoacids3' : form_name
}

### Corresponde al formato IUPAC extended protein que aparece en Biopython

def to_aminoacids1_seq(item, atom_indices=None, frame_indices=None):

    from Bio.SeqUtils import seq1
    from .api_aminoacids1 import extract_subsystem as extract_seq1
    tmp_item = seq1(item.replace('aminoacids3:',''))
    tmp_item = extract_seq1(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_biopython_Seq(item, atom_indices=None, frame_indices=None):

    from .api_aminoacids1 import to_biopython_Seq as aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = _aminoacis1_to_biopython_Seq(tmp_item)
    return tmp_item

def to_biopython_SeqRecord(item, atom_indices=None, frame_indices=None):

    from .api_aminoacids1 import to_biopython_SeqRecord as aminoacids1_to_biopython_SeqRecord
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacis1_to_biopython_SeqRecord(tmp_item)
    return tmp_item

def to_fasta(item, output_file_path=None, atom_indices=None, frame_indices=None):

    from .api_aminoacids1 import to_fasta as aminoacids1_to_fasta
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return aminoacis1_to_fasta(tmp_item, output_file_path=output_file_path)

def get_shape(item):
    raise NotImplementedError

def select_with_MDTraj(item, selection):
    raise NotImplementedError

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

