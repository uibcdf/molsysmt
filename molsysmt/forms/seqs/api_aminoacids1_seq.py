from os.path import basename as _basename

form_name='aminoacids1:seq'

is_form={
    'aminoacids1:seq' : form_name,
    'aminoacids1' : form_name
}

info=["",""]
with_topology=True

### Corresponde al formato IUPAC extended protein que aparece en Biopython

def to_aminoacids3_seq(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from Bio.SeqUtils import seq3
    tmp_item=seq3(item.replace('aminoacids1:',''))
    return 'aminoacids3:'+tmp_item

def to_biopython_Seq(item, atom_indices='all', frame_indices='all',
                     topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.forms.classes.api_biopython_Seq import extract as extract_biopython_Seq
    from Bio.Seq import Seq as bio_Seq
    from Bio.Alphabet.IUPAC import ExtendedIUPACProtein
    tmp_item = bio_Seq(item.replace('aminoacids1:',''), ExtendedIUPACProtein())
    tmp_item = extract_biopython_Seq(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_biopython_SeqRecord(item, atom_indices='all', frame_indices='all',
                           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
                           id=None, name=None, description=None):

    from molsysmt.forms.classes.api_biopython_Seq import to_biopython_SeqRecord as Seq_to_SeqRecord
    tmp_item=to_biopython_Seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item=Seq_to_SeqRecord(tmp_item)
    return tmp_item

def to_fasta(item, atom_indices='all', frame_indices='all',
             topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
             output_filename=None):

    from molsysmt.forms.classes.api_biopython_SeqRecord import to_fasta as SeqRecord_to_fasta
    tmp_item=to_biopython_SeqRecord(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return SeqRecord_to_fasta(tmp_item, output_filename)

def to_pir(item, atom_indices='all', frame_indices='all',
             topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
             output_filename=None, id=None, style=None):

    from molsysmt.forms.classes.api_biopython_SeqRecord import to_pir as SeqRecord_to_pir
    tmp_item= to_biopython_SeqRecord(item, id=id, atom_indices=atom_indices, frame_indices=frame_indices)
    return SeqRecor_to_pir(tmp_item, output_filename=output_filename, style=style)

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    return item

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

