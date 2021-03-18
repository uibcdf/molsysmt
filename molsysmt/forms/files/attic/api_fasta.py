rom molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np

form_name='fasta'

is_form = {
    }

info=["",""]
with_topology=True
with_trajectory=False
with_coordinates=False
with_box=False
with_bonds=False
with_parameters=False

def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', frame_indices='all'):

    from Bio.SeqIO import read as Bio_SeqRecord_reader
    from molsysmt.forms.classes.api_Bio_SeqRecord import extract as extract_Bio_SeqRecord

    tmp_item=Bio_SeqRecord_reader(item,'fasta')
    tmp_item=extract_Bio_SeqRecord(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

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

