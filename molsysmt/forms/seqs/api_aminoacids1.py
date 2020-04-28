from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','')+':seq'

is_form={
    'aminoacids1:seq' : form_name,
    'aminoacids1' : form_name
}

info=["",""]

### Corresponde al formato IUPAC extended protein que aparece en Biopython

def to_aminoacids3_seq(item, atom_indices='all', frame_indices='all'):
    from Bio.SeqUtils import seq3
    tmp_item=seq3(item.replace('aminoacids1:',''))
    return 'aminoacids3:'+tmp_item

def to_biopython_Seq(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_biopython_Seq import extract_subsystem as extract_biopython_Seq
    from Bio.Seq import Seq as bio_Seq
    from Bio.Alphabet.IUPAC import ExtendedIUPACProtein
    tmp_item = bio_Seq(item.replace('aminoacids1:',''), ExtendedIUPACProtein())
    tmp_item = extract_biopython_Seq(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_biopython_SeqRecord(item, id=None, name=None, description=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_biopython_Seq import to_biopython_SeqRecord as Seq_to_SeqRecord
    tmp_item=to_biopython_Seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item=Seq_to_SeqRecord(tmp_item)
    return tmp_item

def to_fasta(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_biopython_SeqRecord import to_fasta as SeqRecord_to_fasta
    tmp_item=to_biopython_SeqRecord(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return SeqRecord_to_fasta(tmp_item, output_file_path)

def to_pir(item, output_file_path=None, id=None, style=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_biopython_SeqRecord import to_pir as SeqRecord_to_pir
    tmp_item= to_biopython_SeqRecord(item, id=id, atom_indices=atom_indices, frame_indices=frame_indices)
    return SeqRecor_to_pir(tmp_item, output_file_path=output_file_path, style=style)

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

