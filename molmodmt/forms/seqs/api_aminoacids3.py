from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','')+':seq'

is_form={
    'aminoacids3:seq' : form_name,
    'aminoacids3' : form_name
}

### Corresponde al formato IUPAC extended protein que aparece en Biopython

def to_aminoacids1_seq(item, atom_indices=None, frame_indices=None):
    from Bio.SeqUtils import seq1
    tmp_seq=seq1(item.replace('aminoacids3:',''))
    tmp_item=tmp_seq
    del(seq1,tmp_seq)
    return tmp_item

def to_biopython_Seq(item, atom_indices=None, frame_indices=None):
    from .api_aminoacids1 import to_biopython_Seq as _aminoacids1_to_biopython_Seq
    tmp_item=to_aminoacids1_seq(item)
    tmp_item=_aminoacis1_to_biopython_Seq(tmp_item)
    del(_aminoacids1_to_biopython_Seq)
    return tmp_item

def to_biopython_SeqRecord(item, atom_indices=None, frame_indices=None):
    from .api_aminoacids1 import to_biopython_SeqRecord as _aminoacids1_to_biopython_SeqRecord
    tmp_item=to_aminoacids1_seq(item)
    tmp_item=_aminoacis1_to_biopython_SeqRecord(tmp_item)
    del(_aminoacids1_to_biopython_SeqRecord)
    return tmp_item


def to_fasta(item, output_file, atom_indices=None, frame_indices=None):
    from .api_aminoacids1 import to_fasta as _aminoacids1_to_fasta
    tmp_item=to_aminoacids1_seq(item)
    return _aminoacis1_to_fasta(tmp_item, output_file)

def get_shape(item):
    raise NotImplementedError

def select_with_MDTraj(item, selection):
    raise NotImplementedError

def extract_subsystem(item, atom_indices=None, frame_indices=None):
    raise NotImplementedError
