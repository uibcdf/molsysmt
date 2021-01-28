from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','')+':seq'

is_form={
    'aminoacids3:seq' : form_name,
    'aminoacids3' : form_name
}

info=["",""]
with_topology=True
with_trajectory=False

### Corresponde al formato IUPAC extended protein que aparece en Biopython

def to_aminoacids3_seq(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    if atom_indices is 'all':
        return item
    else:
        raise NotImplementedError

def to_aminoacids1_seq(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from Bio.SeqUtils import seq1
    tmp_item = seq1(item.replace('aminoacids3:',''))
    return 'aminoacids1:'+tmp_item

def to_biopython_Seq(item, atom_indices='all', frame_indices='all',
                     topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from .api_aminoacids1 import to_biopython_Seq as aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = _aminoacis1_to_biopython_Seq(tmp_item)
    return tmp_item

def to_biopython_SeqRecord(item, atom_indices='all', frame_indices='all',
                           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from .api_aminoacids1 import to_biopython_SeqRecord as aminoacids1_to_biopython_SeqRecord
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacis1_to_biopython_SeqRecord(tmp_item)
    return tmp_item

def to_fasta(item, atom_indices='all', frame_indices='all',
             topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
             output_filename=None):

    from .api_aminoacids1 import to_fasta as aminoacids1_to_fasta
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return aminoacis1_to_fasta(tmp_item, output_filename=output_filename)

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt import build_peptide
    from molsysmt.forms.classes.api_molsysmt_MolSys import extract as extract_molsysmt_MolSys

    tmp_item = build_peptide(item, to_form='molsysmt.MolSys')
    tmp_item = extract_molsysmt_MolSys(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_nglview_NGLWidget(item, atom_indices='all', frame_indices='all',
                         topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    return to_NGLView(item, topology_item=topology_item, trajectory_item=trajectory_item,
            atom_indices=atom_indices, frame_indices=frame_indices)

def to_NGLView(item, atom_indices='all', frame_indices='all',
               topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_NGLView as molsysmt_MolSys_to_NGLView

    tmp_item = to_molsysmt_MolSys(item, topology_item=topology_item,
            trajectory_item=trajectory_item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = molsysmt_MolSys_to_NGLView(tmp_item)

    return tmp_item

def select_with_MDTraj(item, selection):
    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):
    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    return item


###### Get

## atom

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return get_form_from_system(item)

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

